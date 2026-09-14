# Image Processing Lab — Version 3

A browser-based Image Processing Lab with **10 essential practical modules**, built with Python, Flask, OpenCV and NumPy.

## What is fixed in this version
- Fixed the OpenCV **Bad number of channels** error that occurred after grayscale operations such as Huffman. Histogram generation now safely accepts both grayscale and BGR images.
- Huffman now performs a real encode → bit-pack → decode → pixel-by-pixel lossless verification workflow.
- RLE performs a real encode/decode reconstruction and verification.
- Correlation Detection uses real OpenCV normalized template matching with a score and bounding box.
- RGB output no longer swaps channels when the result is saved.
- Better validation for second images, masks, templates and Canny thresholds.
- Fresh beige/cream interface with dark charcoal text, muted green and warm brown accents.
- Responsive design for laptops and phones.

## 10 practicals
1. Image Operations
2. Geometric Transformation
3. Spatial Enhancement
4. Spatial Filters
5. Image Inpainting
6. Lossless Compression
7. Morphological Operations
8. Correlation Detection
9. Colour Spaces
10. Edge Detection

## Run locally
```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Run:
```bash
python app.py
```

Open:
`http://127.0.0.1:5000`

## GitHub + Render
Upload the contents of this `image_processing_lab` folder to GitHub. Render can use:
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

The included `render.yaml` can also be used as the deployment configuration.

## Important for Template Matching
Upload the main scene as the first image and the smaller object/template as the second image.

## Important for Inpainting
Upload the damaged image as the first image and a mask as the second image. White pixels in the mask indicate the area to repair.
