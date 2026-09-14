import os
import cv2
import numpy as np
import heapq
import base64
import json
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOAD = os.path.join(BASE, "uploads")
OUTPUT = os.path.join(BASE, "outputs")
os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
ALLOWED = {"png", "jpg", "jpeg", "bmp", "webp"}


def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED


def read_img(path):
    data = np.fromfile(path, dtype=np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)


def save_img(img, path):
    if img is None:
        raise ValueError("Processing returned no image.")
    if img.dtype != np.uint8:
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    if img.ndim not in (2, 3):
        raise ValueError("Unsupported output image format.")
    ext = os.path.splitext(path)[1] or ".png"
    params = [cv2.IMWRITE_JPEG_QUALITY, 95] if ext.lower() in {".jpg", ".jpeg"} else []
    ok, buf = cv2.imencode(ext, img, params)
    if not ok:
        raise ValueError("Could not encode output image.")
    buf.tofile(path)


def gray(img):
    """Convert to grayscale only when needed; fixes OpenCV channel errors."""
    if img is None:
        raise ValueError("Image is empty.")
    if img.ndim == 2:
        return img
    if img.ndim == 3 and img.shape[2] == 1:
        return img[:, :, 0]
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def odd(value):
    n = max(3, int(float(value)))
    return n if n % 2 else n + 1


def resized_second(img, second):
    if second is None:
        return img
    return cv2.resize(second, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)


def overlay_box(img, x, y, w, h, score):
    out = img.copy()
    cv2.rectangle(out, (x, y), (x + w, y + h), (54, 170, 92), 3)
    label = f"Match {score:.3f}"
    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.62, 2)
    top = max(th + 10, y)
    cv2.rectangle(out, (x, top - th - 12), (x + tw + 16, top + 5), (48, 48, 43), -1)
    cv2.putText(out, label, (x + 8, top - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (255, 255, 255), 2, cv2.LINE_AA)
    return out


# ---------------- Lossless compression ----------------
def build_huffman_codes(freq):
    if not freq:
        return {}
    if len(freq) == 1:
        return {next(iter(freq)): "0"}

    heap = []
    uid = 0
    for symbol, count in sorted(freq.items()):
        heap.append((count, uid, ("leaf", symbol)))
        uid += 1
    heapq.heapify(heap)

    while len(heap) > 1:
        c1, _, n1 = heapq.heappop(heap)
        c2, _, n2 = heapq.heappop(heap)
        heapq.heappush(heap, (c1 + c2, uid, ("node", n1, n2)))
        uid += 1

    root = heap[0][2]
    codes = {}

    def walk(node, prefix=""):
        if node[0] == "leaf":
            codes[node[1]] = prefix or "0"
            return
        walk(node[1], prefix + "0")
        walk(node[2], prefix + "1")

    walk(root)
    return codes


def huffman_roundtrip(g):
    flat = g.ravel().tolist()
    freq = {}
    for value in flat:
        freq[value] = freq.get(value, 0) + 1

    codes = build_huffman_codes(freq)
    bitstream = "".join(codes[value] for value in flat)
    pad = (8 - len(bitstream) % 8) % 8
    packed = bytes(int(bitstream[i:i + 8].ljust(8, "0"), 2) for i in range(0, len(bitstream), 8))

    reverse = {code: symbol for symbol, code in codes.items()}
    decoded = []
    current = ""
    for bit in bitstream:
        current += bit
        if current in reverse:
            decoded.append(reverse[current])
            current = ""

    if len(decoded) != g.size:
        raise ValueError("Huffman decode verification failed.")

    reconstructed = np.array(decoded, dtype=np.uint8).reshape(g.shape)
    verified = bool(np.array_equal(g, reconstructed))

    raw_bits = int(g.size * 8)
    encoded_bits = int(len(bitstream))
    padding_bits = int(pad)
    # Educational header estimate: symbol + frequency count for each used grayscale value.
    header_bits = int(len(freq) * 40)
    total_bits = encoded_bits + padding_bits + header_bits
    ratio = raw_bits / total_bits if total_bits else 0

    return reconstructed, {
        "method": "Huffman",
        "symbols": len(freq),
        "raw_bits": raw_bits,
        "encoded_data_bits": encoded_bits,
        "header_estimate_bits": header_bits,
        "padding_bits": padding_bits,
        "estimated_total_bits": total_bits,
        "average_bits_per_pixel": round(encoded_bits / g.size, 3),
        "compression_ratio": round(ratio, 3),
        "lossless_verified": verified,
        "packed_bytes": len(packed),
        "note": "Educational header estimate; decoded pixels are compared with the original."
    }


def rle_roundtrip(g):
    flat = g.ravel().tolist()
    runs = []
    if flat:
        value, count = flat[0], 1
        for item in flat[1:]:
            if item == value:
                count += 1
            else:
                runs.append((value, count))
                value, count = item, 1
        runs.append((value, count))

    decoded = []
    for value, count in runs:
        decoded.extend([value] * count)
    reconstructed = np.array(decoded, dtype=np.uint8).reshape(g.shape)

    raw_bits = int(g.size * 8)
    encoded_bits = int(len(runs) * 40)
    return reconstructed, {
        "method": "RLE",
        "pixels": int(g.size),
        "runs": len(runs),
        "raw_bits": raw_bits,
        "encoded_bits": encoded_bits,
        "compression_ratio": round(raw_bits / encoded_bits, 3) if encoded_bits else 0,
        "lossless_verified": bool(np.array_equal(g, reconstructed)),
        "note": "RLE is strongest when adjacent pixels repeat in long runs."
    }


# ---------------- Processing ----------------
def process(img, op, p, second=None):
    if op == "grayscale":
        return gray(img), "Grayscale image", {}
    if op == "negative":
        return 255 - img, "Negative image", {}

    if op == "threshold":
        g = gray(img)
        t = int(p.get("threshold", 128))
        mode = p.get("type", "binary")
        mapping = {
            "binary": cv2.THRESH_BINARY,
            "inverse": cv2.THRESH_BINARY_INV,
            "trunc": cv2.THRESH_TRUNC,
            "tozero": cv2.THRESH_TOZERO,
            "tozero_inv": cv2.THRESH_TOZERO_INV,
        }
        _, out = cv2.threshold(g, t, 255, mapping.get(mode, cv2.THRESH_BINARY))
        return out, "Threshold result", {"threshold": t, "type": mode}

    if op in {"bitwise_and", "bitwise_or", "bitwise_xor", "add", "subtract"}:
        if second is None:
            raise ValueError("Upload a second image for this operation.")
        b = resized_second(img, second)
        if op == "bitwise_and":
            out = cv2.bitwise_and(img, b)
        elif op == "bitwise_or":
            out = cv2.bitwise_or(img, b)
        elif op == "bitwise_xor":
            out = cv2.bitwise_xor(img, b)
        elif op == "add":
            out = cv2.add(img, b)
        else:
            out = cv2.subtract(img, b)
        return out, op.replace("_", " ").title(), {}

    if op == "resize":
        scale = max(0.1, min(4.0, float(p.get("scale", 1))))
        out = cv2.resize(img, None, fx=scale, fy=scale,
                         interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC)
        return out, f"Resized ×{scale:g}", {"scale": scale}

    if op == "rotate":
        angle = float(p.get("angle", 0))
        h, w = img.shape[:2]
        matrix = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
        out = cv2.warpAffine(img, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)
        return out, f"Rotation {angle:g}°", {"angle": angle}

    if op == "translate":
        x, y = int(p.get("x", 30)), int(p.get("y", 30))
        h, w = img.shape[:2]
        matrix = np.float32([[1, 0, x], [0, 1, y]])
        out = cv2.warpAffine(img, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)
        return out, "Translation", {"x": x, "y": y}

    if op == "flip":
        mode = {"horizontal": 1, "vertical": 0, "both": -1}.get(p.get("mode", "horizontal"), 1)
        return cv2.flip(img, mode), "Flip", {"direction": p.get("mode", "horizontal")}

    if op == "affine":
        h, w = img.shape[:2]
        dx = min(int(p.get("dx", 40)), max(1, w // 3))
        dy = min(int(p.get("dy", 30)), max(1, h // 3))
        src = np.float32([[0, 0], [w - 1, 0], [0, h - 1]])
        dst = np.float32([[dx, dy], [w - 1 - dx, dy], [dx, h - 1 - dy]])
        matrix = cv2.getAffineTransform(src, dst)
        return cv2.warpAffine(img, matrix, (w, h), borderMode=cv2.BORDER_REFLECT), "Affine transformation", {}

    if op == "perspective":
        h, w = img.shape[:2]
        d = max(0, min(0.3, float(p.get("perspective", 0.12))))
        q = int(min(w, h) * d)
        src = np.float32([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]])
        dst = np.float32([[q, q], [w - 1 - q, 0], [w - 1, h - 1 - q], [0, h - 1]])
        matrix = cv2.getPerspectiveTransform(src, dst)
        return cv2.warpPerspective(img, matrix, (w, h), borderMode=cv2.BORDER_REFLECT), "Perspective transformation", {}

    if op == "hist_eq":
        return cv2.equalizeHist(gray(img)), "Histogram equalization", {}

    if op == "clahe":
        clip = max(1.0, min(8.0, float(p.get("clip", 2))))
        clahe = cv2.createCLAHE(clipLimit=clip, tileGridSize=(8, 8))
        return clahe.apply(gray(img)), "CLAHE", {"clip_limit": clip}

    if op == "gamma":
        gamma = max(0.1, min(5, float(p.get("gamma", 1))))
        table = np.array([((i / 255.0) ** (1 / gamma)) * 255 for i in range(256)], dtype=np.uint8)
        return cv2.LUT(img, table), f"Gamma {gamma:g}", {"gamma": gamma}

    if op == "log":
        x = img.astype(np.float32)
        maximum = float(np.max(x)) or 1.0
        c = 255.0 / np.log1p(maximum)
        return np.uint8(c * np.log1p(x)), "Log transformation", {}

    if op == "unsharp":
        k = odd(p.get("kernel", 5))
        amount = max(0.1, min(3, float(p.get("amount", 1.5))))
        blur = cv2.GaussianBlur(img, (k, k), 0)
        return cv2.addWeighted(img, 1 + amount, blur, -amount, 0), "Unsharp masking", {"kernel": k, "amount": amount}

    if op in {"mean", "gaussian", "median", "bilateral"}:
        k = odd(p.get("kernel", 5))
        if op == "mean":
            return cv2.blur(img, (k, k)), "Mean filter", {"kernel": k}
        if op == "gaussian":
            return cv2.GaussianBlur(img, (k, k), 0), "Gaussian filter", {"kernel": k}
        if op == "median":
            return cv2.medianBlur(img, k), "Median filter", {"kernel": k}
        return cv2.bilateralFilter(img, k, 75, 75), "Bilateral filter", {"kernel": k}

    if op == "laplacian":
        return cv2.convertScaleAbs(cv2.Laplacian(gray(img), cv2.CV_64F)), "Laplacian filter", {}

    if op in {"sobel", "prewitt"}:
        g = gray(img)
        if op == "sobel":
            x = cv2.Sobel(g, cv2.CV_64F, 1, 0, ksize=3)
            y = cv2.Sobel(g, cv2.CV_64F, 0, 1, ksize=3)
        else:
            kx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float64)
            ky = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float64)
            x, y = cv2.filter2D(g, cv2.CV_64F, kx), cv2.filter2D(g, cv2.CV_64F, ky)
        mag = cv2.magnitude(x.astype(np.float32), y.astype(np.float32))
        return cv2.convertScaleAbs(mag), op.title() + " filter", {}

    if op in {"telea", "ns"}:
        if second is None:
            raise ValueError("Upload a mask image. White areas in the mask are the damaged areas to repair.")
        mask = gray(resized_second(img, second))
        _, mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
        method = cv2.INPAINT_TELEA if op == "telea" else cv2.INPAINT_NS
        radius = max(1, min(10, float(p.get("radius", 3))))
        return cv2.inpaint(img, mask, radius, method), op.upper() + " inpainting", {"radius": radius}

    if op == "rle":
        out, extra = rle_roundtrip(gray(img))
        return out, "RLE lossless reconstruction", extra

    if op == "huffman":
        out, extra = huffman_roundtrip(gray(img))
        return out, "Huffman lossless reconstruction", extra

    if op in {"erosion", "dilation", "opening", "closing", "gradient", "tophat", "blackhat"}:
        g = gray(img)
        threshold = int(p.get("threshold", 128))
        _, binary = cv2.threshold(g, threshold, 255, cv2.THRESH_BINARY)
        k = odd(p.get("kernel", 5))
        iterations = max(1, int(p.get("iterations", 1)))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (k, k))
        code = {
            "erosion": cv2.MORPH_ERODE,
            "dilation": cv2.MORPH_DILATE,
            "opening": cv2.MORPH_OPEN,
            "closing": cv2.MORPH_CLOSE,
            "gradient": cv2.MORPH_GRADIENT,
            "tophat": cv2.MORPH_TOPHAT,
            "blackhat": cv2.MORPH_BLACKHAT,
        }[op]
        out = cv2.morphologyEx(binary, code, kernel, iterations=iterations)
        return out, op.title(), {"kernel": k, "threshold": threshold, "iterations": iterations}

    if op == "template":
        if second is None:
            raise ValueError("Upload a smaller template image to find inside the main image.")
        scene = gray(img)
        template = gray(second)
        if template.size == 0:
            raise ValueError("Template image is empty.")

        if template.shape[0] > scene.shape[0] or template.shape[1] > scene.shape[1]:
            scale = min(scene.shape[1] / template.shape[1], scene.shape[0] / template.shape[0])
            template = cv2.resize(template, None, fx=max(0.05, scale * 0.9), fy=max(0.05, scale * 0.9), interpolation=cv2.INTER_AREA)
        if template.shape[0] < 2 or template.shape[1] < 2:
            raise ValueError("Template is too small after resizing.")

        # Avoid undefined CCOEFF results for a completely flat template.
        if float(np.std(template)) < 1e-6:
            method = cv2.TM_SQDIFF_NORMED
            result = cv2.matchTemplate(scene, template, method)
            minimum, _, location, _ = cv2.minMaxLoc(result)
            score = 1.0 - float(minimum)
        else:
            method = cv2.TM_CCOEFF_NORMED
            result = cv2.matchTemplate(scene, template, method)
            _, score, _, location = cv2.minMaxLoc(result)

        score = float(np.clip(score, 0, 1))
        th, tw = template.shape
        out = overlay_box(img, location[0], location[1], tw, th, score)
        return out, f"Template matching • score {score:.3f}", {
            "score": round(score, 4),
            "x": int(location[0]),
            "y": int(location[1]),
            "template_width": int(tw),
            "template_height": int(th),
            "method": "Normalized cross-correlation"
        }

    if op == "rgb":
        # The uploaded source is BGR internally; returning it unchanged preserves correct RGB appearance when saved.
        return img.copy(), "RGB colour image", {"channels": 3}

    if op == "hsv":
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR), "HSV visualized", {"channels": 3}

    if op == "lab":
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR), "LAB visualized", {"channels": 3}

    if op == "ycrcb":
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR), "YCrCb visualized", {"channels": 3}

    if op == "canny":
        low = int(p.get("low", 80))
        high = max(low + 1, int(p.get("high", 160)))
        return cv2.Canny(gray(img), low, high), "Canny edges", {"low": low, "high": high}

    if op == "roberts":
        g = gray(img)
        x = cv2.filter2D(g, cv2.CV_64F, np.array([[1, 0], [0, -1]], dtype=float))
        y = cv2.filter2D(g, cv2.CV_64F, np.array([[0, 1], [-1, 0]], dtype=float))
        return cv2.convertScaleAbs(cv2.magnitude(x.astype(np.float32), y.astype(np.float32))), "Roberts edges", {}

    raise ValueError("Unsupported operation.")


def image_data_url(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def histogram_data(img):
    g = gray(img)  # Safe for both BGR and already-grayscale outputs.
    hist = cv2.calcHist([g], [0], None, [32], [0, 256]).flatten()
    maximum = float(hist.max() or 1)
    return [round(float(v / maximum), 4) for v in hist]


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify(status="ok", service="Image Processing Lab", version="3.0")


@app.post("/process")
def process_route():
    try:
        uploaded = request.files.get("image")
        operation = request.form.get("operation", "grayscale")

        if not uploaded or not uploaded.filename or not allowed(uploaded.filename):
            return jsonify(error="Please upload a valid PNG/JPG/JPEG/BMP/WEBP image."), 400

        safe_name = secure_filename(uploaded.filename)
        source_path = os.path.join(UPLOAD, f"{uuid.uuid4().hex}_{safe_name}")
        uploaded.save(source_path)
        img = read_img(source_path)
        if img is None:
            return jsonify(error="Could not read the uploaded image."), 400

        second = None
        second_file = request.files.get("second")
        if second_file and second_file.filename:
            if not allowed(second_file.filename):
                return jsonify(error="Second file must be an image."), 400
            second_name = secure_filename(second_file.filename)
            second_path = os.path.join(UPLOAD, f"{uuid.uuid4().hex}_{second_name}")
            second_file.save(second_path)
            second = read_img(second_path)
            if second is None:
                return jsonify(error="Could not read the second image."), 400

        params = {key: value for key, value in request.form.items()}
        out, title, extra = process(img, operation, params, second)

        output_name = f"result_{uuid.uuid4().hex}.png"
        output_path = os.path.join(OUTPUT, output_name)
        save_img(out, output_path)

        h, w = img.shape[:2]
        oh, ow = out.shape[:2]
        return jsonify({
            "ok": True,
            "title": title,
            "url": "/output/" + output_name,
            "download": "/download/" + output_name,
            "extra": extra,
            "input_size": f"{w} × {h}",
            "output_size": f"{ow} × {oh}",
            "histogram": histogram_data(img),
            "output_histogram": histogram_data(out),
            "output_data": image_data_url(output_path)
        })
    except Exception as exc:
        return jsonify(error=str(exc)), 500


@app.get("/output/<name>")
def output(name):
    return send_from_directory(OUTPUT, name)


@app.get("/download/<name>")
def download(name):
    return send_from_directory(OUTPUT, name, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
