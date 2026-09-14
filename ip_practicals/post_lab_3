# import cv2
# import matplotlib.pyplot as plt
# import numpy as np
#
# image_path = "I1.jpg"
#
# image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#
# if image is None:
#     print("Error: Image not found")
#     exit()
#
# blurred_image = cv2.GaussianBlur(image, (5, 5), 1.4)
#
# edges = cv2.Canny(blurred_image, 50, 150)
#
# plt.figure(figsize=(10, 5))
#
# plt.subplot(1, 2, 1)
# plt.title("Original Image")
# plt.imshow(image, cmap="gray")
# plt.axis("off")
#
# plt.subplot(1, 2, 2)
# plt.title("Edge Detected Image || CS24070")
# plt.imshow(edges, cmap="gray")
# plt.axis("off")
#
# plt.show()


# import cv2
#
# img = cv2.imread("I1.jpg")
#
# t_lower = 50
# t_upper = 150
#
# edge = cv2.Canny(img, t_lower, t_upper)
#
# cv2.imshow('original || CS24070', img)
# cv2.imshow('edge || CS24070', edge)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# import cv2
#
# img = cv2.imread("I1.jpg")
#
# t_lower = 100
# t_upper = 200
# aperture_size = 5
#
# edge = cv2.Canny(img, t_lower, t_upper, apertureSize=aperture_size)
#
# cv2.imshow('original', img)
# cv2.imshow('Canny with Aperture Size CS24070', edge)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# import cv2
#
# img = cv2.imread("I1.jpg")
#
# t_lower = 100
# t_upper = 200
# aperture_size = 5
# L2Gradient = True
#
# edge = cv2.Canny(img, t_lower, t_upper, L2gradient=L2Gradient)
#
# cv2.imshow('original', img)
# cv2.imshow('Canny with L2Gradient CS24070', edge)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
#
# img = cv2.imread('I1.jpg', cv2.IMREAD_GRAYSCALE)
#
# if img is None:
#     raise ValueError("Image not found. Please check the path and filename.")
#
# sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
# sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
#
# sobel_edges = cv2.magnitude(sobelx, sobely)
# sobel_edges = np.uint8(sobel_edges)
#
# plt.figure(figsize=(10, 4))
# plt.subplot(1, 2, 1)
# plt.imshow(img, cmap='gray')
# plt.title('Original Image')
# plt.axis('off')
#
# plt.subplot(1, 2, 2)
# plt.imshow(sobel_edges, cmap='gray')
# plt.title('Sobel Edges CS24070')
# plt.axis('off')
#
# plt.tight_layout()
# plt.show()
#
# cv2.imwrite('sobel_edges.jpg', sobel_edges)

import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('I1.jpg', cv2.IMREAD_GRAYSCALE)

if img is None:
    raise ValueError("Image not found. Please check the path and filename.")

kernelx = np.array([
    [-1, 0, 1],
    [-1, 0, 1],
    [-1, 0, 1]
], dtype=np.float32)

kernely = np.array([
    [-1, -1, -1],
    [0, 0, 0],
    [1, 1, 1]
], dtype=np.float32)

prewittx = cv2.filter2D(img, cv2.CV_64F, kernelx)
prewitty = cv2.filter2D(img, cv2.CV_64F, kernely)

prewitt_edges = cv2.magnitude(prewittx, prewitty)
prewitt_edges = np.uint8(prewitt_edges)

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray')
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(prewitt_edges, cmap='gray')
plt.title('Prewitt Edges CS24070')
plt.axis('off')

plt.tight_layout()
plt.show()

cv2.imwrite('prewitt_edges.jpg', prewitt_edges)
