# import numpy as np
# import cv2 as cv
# img = cv.imread("I2.jpg",0)
# rows, cols = img.shape
# M = np.float32([[1, 0, 100], [0, 1, 50]])
# dst = cv.warpAffine(img, M, (cols, rows))
# cv.imshow("Manish", dst)
# cv.waitKey(0)
# cv.destroyAllWindows()


# import numpy as np
# import cv2 as cv
# img = cv.imread("I2.jpg", 0)
# rows, cols = img.shape
# M = np.float32([[1, 0, 0],
# [0, -1, rows],
# [0, 0, 1]])
# reflected_img = cv.warpPerspective(img, M,
#                                    (int(cols),
#                                     int(rows)))
# cv.imshow("MANISH", reflected_img)
# cv.imwrite("reflection_out.jpg", reflected_img)
# cv.waitKey(0)
# cv.destroyAllWindows()


# import numpy as np
# import cv2 as cv
# img = cv.imread("I2.jpg", 0)
# rows, cols = img.shape
# M = np.float32([[1, 0, 0], [0, -1, rows], [0, 0, 1]])
# img_rotation = cv.warpAffine(img,
# cv.getRotationMatrix2D((cols/2, rows/2),
# 30, 0.6),
# (cols, rows))
# cv.imshow("Manish", img_rotation)
# cv.imwrite("rotation_out.jpg", img_rotation)
# cv.waitKey(0)
# cv.destroyAllWindows()


# # import numpy as np
# import cv2 as cv
# img = cv.imread("I2.jpg", 0)
# rows, cols = img.shape
# img_shrinked = cv.resize(img, (200, 100),
# interpolation=cv.INTER_AREA)
# cv.imshow("Manish", img_shrinked)
# img_enlarged = cv.resize(img_shrinked, None,
# fx=1.5, fy=1.5,
# interpolation=cv.INTER_CUBIC)
# cv.imshow("Manish", img_enlarged)
# cv.waitKey(0)
# cv.destroyAllWindows()

# import numpy as np
# import cv2 as cv
# img = cv.imread("I2.jpg", 0)
# cropped_img = img[100:300, 100:300]
# cv.imwrite("cropped_out.jpg", cropped_img)
# cv.waitKey(0)
# cv.destroyAllWindows()

# import numpy as np
# import cv2 as cv
# img = cv.imread("I2.jpg", 0)
# rows, cols = img.shape
# M = np.float32([[1, 0.5, 0], [0, 1, 0], [0, 0, 1]])
# sheared_img = cv.warpPerspective(img, M, (int(cols*1.5), int(rows*1.5)))
# cv.imshow("Arif", sheared_img)
# cv.waitKey(0)
# cv.destroyAllWindows()


import numpy as np
import cv2 as cv
img = cv.imread("I2.jpg", 0)
rows, cols = img.shape
M = np.float32([[1, 0, 0], [0.5, 1, 0], [0, 0, 1]])
sheared_img = cv.warpPerspective(img, M, (int(cols*1.5), int(rows*1.5)))
cv.imshow("Arif", sheared_img)
cv.waitKey(0)
cv.destroyAllWindows()
