# import cv2
# import numpy as np
# img = cv2.imread("I1.jpg", 0)
# negative = 255 - img
# combined = np.hstack((img, negative))
# cv2.imshow("Arif", combined)
# cv2.waitKey(0)
# cv2.destroyAllWindows


# import cv2
# import matplotlib.pyplot as plt
# import numpy as np
# image = cv2.imread("I1.jpg")
# brightness = 10
# contrast = 2.3
# image2 = cv2.addWeighted(
#     image,
#     contrast,
#     np.zeros(image.shape, image.dtype),
#     0,
#     brightness
# )
# plt.subplot(1,2,1)
# plt.title("Original")
# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
# plt.subplot(1,2,2)
# plt.title("Modified")
# plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
# plt.show()

# import cv2
# import matplotlib.pyplot as plt
#
# image = cv2.imread("I1.jpg")
#
# alpha = 1.5
# beta = 50
#
# image2 = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
#
# plt.subplot(1,2,1)
# plt.title("Original")
# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#
# plt.subplot(1,2,2)
# plt.title("Modified")
# plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
#
# plt.show()

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
#
# image = cv2.imread("I1.jpg")
#
# kernel = np.array([[0,-1,0],
#                    [-1,5,-1],
#                    [0,-1,0]])
#
# sharpen = cv2.filter2D(image, -1, kernel)
#
# plt.subplot(1,2,1)
# plt.title("Original")
# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#
# plt.subplot(1,2,2)
# plt.title("Sharpen")
# plt.imshow(cv2.cvtColor(sharpen, cv2.COLOR_BGR2RGB))
#
# plt.show()

# import cv2
# import matplotlib.pyplot as plt
#
# image = cv2.imread("I1.jpg")
#
# lap = cv2.Laplacian(image, cv2.CV_64F)
#
# plt.subplot(1,2,1)
# plt.title("Original")
# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#
# plt.subplot(1,2,2)
# plt.title("Laplacian")
# plt.imshow(lap.astype("uint8"))
#
# plt.show()


# import cv2
# import matplotlib.pyplot as plt
#
# image = cv2.imread("I1.jpg")
#
# filtered = cv2.medianBlur(image, 11)
#
# plt.subplot(1,2,1)
# plt.title("Original")
# plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#
# plt.subplot(1,2,2)
# plt.title("Median Blur")
# plt.imshow(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
#
# plt.show()

# import cv2
# import numpy as np
# img = cv2.imread("I1.jpg", 0)
# equ = cv2.equalizeHist(img)
# result = np.hstack((img, equ))
# cv2.imshow("Arif", result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# img = cv2.imread("I1.jpg", 0)
# equ = cv2.equalizeHist(img)
# result = np.hstack((img, equ))
# cv2.imshow("MANISH", result)
# plt.figure(figsize=(10,5))
#
# plt.subplot(1,2,1)
# plt.hist(img.ravel(),256,[0,256])
# plt.title("Original Histogram")
#
# plt.subplot(1,2,2)
# plt.hist(equ.ravel(),256,[0,256])
# plt.title("Equalized Histogram")
#
# plt.show()
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2

# Read image
image = cv2.imread("I1.jpg")

# Check image
if image is None:
    print("Image not found!")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Thresholding
_, thresh1 = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
_, thresh2 = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
_, thresh3 = cv2.threshold(gray, 120, 255, cv2.THRESH_TRUNC)
_, thresh4 = cv2.threshold(gray, 120, 255, cv2.THRESH_TOZERO)
_, thresh5 = cv2.threshold(gray, 120, 255, cv2.THRESH_TOZERO_INV)

# Display images
cv2.imshow("Original", gray)
cv2.imshow("Binary", thresh1)
cv2.imshow("Binary Inv", thresh2)
cv2.imshow("Truncate", thresh3)
cv2.imshow("To Zero", thresh4)
cv2.imshow("To Zero Inv", thresh5)

cv2.waitKey(0)
cv2.destroyAllWindows()
