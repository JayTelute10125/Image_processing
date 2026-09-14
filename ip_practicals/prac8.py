#code 1
import cv2
import numpy as np

image_path = 'PRA7-1.jpg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if image is None:
    raise FileNotFoundError("Image not found. Check the path.")

_, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

erosion = cv2.erode(binary, kernel, iterations=1)

dilation = cv2.dilate(binary, kernel, iterations=1)

opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

cv2.imshow("Original Binary || CS24091", binary)
cv2.imshow("Erosion|| CS24070", erosion)
cv2.imshow("Dilation|| CS24070", dilation)
cv2.imshow("Opening|| CS24070", opening)
cv2.imshow("Closing|| CS24070", closing)

cv2.waitKey(0)
cv2.destroyAllWindows()

#code 2
import cv2
import numpy as np

image_path = 'PRA7-1.jpg'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if image is None:
    raise FileNotFoundError("Image not found. Check the path.")

_, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

kernel_size = (5, 5)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

morph_ops = {
    "Erosion": cv2.erode(binary, kernel, iterations=1),
    "Dilation": cv2.dilate(binary, kernel, iterations=1),
    "Opening": cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel),
    "Closing": cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
}

def calculate_object_areas(binary_img):
    contours, _ = cv2.findContours(
        binary_img,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    areas = [cv2.contourArea(c) for c in contours]
    return areas, contours

for op_name, op_img in morph_ops.items():
    areas, contours = calculate_object_areas(op_img)
    print(f"{op_name}: Number of objects = {len(areas)}, Areas = {areas}")

    contoured_img = cv2.cvtColor(op_img, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(contoured_img, contours, -1, (0, 0, 255), 2)

    cv2.imshow(f"{op_name} with Contours CS24070", contoured_img)

cv2.imshow("Original Binary CS24070", binary)

cv2.waitKey(0)
cv2.destroyAllWindows()
