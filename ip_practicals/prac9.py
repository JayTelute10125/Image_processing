import cv2
import numpy as np

def detect_object(template_path, input_image_path):

    template = cv2.imread(template_path, 0)
    img = cv2.imread(input_image_path)

    if template is None:
        print("Error: Template image not found!")
        return

    if img is None:
        print("Error: Input image not found!")
        return

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    best_score = -1
    best_location = None
    best_size = None

    scales = np.arange(0.3, 1.01, 0.05)

    for scale in scales:

        new_width = int(template.shape[1] * scale)
        new_height = int(template.shape[0] * scale)

        if new_width < 20 or new_height < 20:
            continue

        resized_template = cv2.resize(
            template,
            (new_width, new_height)
        )

        if (new_width > gray_img.shape[1] or
                new_height > gray_img.shape[0]):
            continue

        result = cv2.matchTemplate(
            gray_img,
            resized_template,
            cv2.TM_CCOEFF_NORMED
        )

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val > best_score:
            best_score = max_val
            best_location = max_loc
            best_size = (new_width, new_height)

    threshold = 0.2

    print("Best Correlation Score:", best_score)

    if best_score >= threshold:

        x, y = best_location
        w, h = best_size

        cv2.rectangle(
            img,
            (x, y),
            (x + w, y + h),
            (0, 255, 255),
            3
        )

        cv2.putText(
            img,
            "Object Detected",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2
        )

        print("Object Detected")

    else:
        print("Object Not Detected")

    cv2.imshow("Detected Objects CS24070", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


template_path = r"C:\Users\Arif Ansari\PycharmProjects\Arif\9-2.png"
input_image_path = r"C:\Users\Arif Ansari\PycharmProjects\Arif\9-1.png"

detect_object(template_path, input_image_path)
