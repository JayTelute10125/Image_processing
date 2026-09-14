# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# img=cv2.imread("IMG2.jpg")
# plt.imshow(img)
# plt.waitforbuttonpress()
# plt.close()


# import cv2
# import numpy as np
# image1 = cv2.imread("I1.jpg")
# image2 = cv2.imread("I2.jpg")
# weightedSum = cv2.addWeighted(image1,0.5, image2,0.5,0)
# cv2.imshow("Manish", weightedSum)
# if cv2.waitKey(0) & 0xff == 27:
#    cv2.destroyAllWindows()


# import cv2
# import numpy as np
# image1 = cv2.imread("I1.jpg")
# image2 = cv2.imread("I2.jpg")
# sub = cv2.subtract(image1, image2)
# cv2.imshow("Manish", sub)
# if cv2.waitKey(0) & 0xff == 27:
#  cv2.destroyAllWindows()


# import cv2
# import numpy as np
# img1 = cv2.imread("I1.jpg")
# img2 = cv2.imread("I2.jpg")
# dest_and = cv2.bitwise_and(img2, img1, mask = None)
# cv2.imshow("Manish", dest_and)
# if cv2.waitKey(0) & 0xff == 27:
#    cv2.destroyAllWindows()

# import cv2
# image_path =r'C:\Users\Manish Kathane\PycharmProjects\Manish\IMG3.jpg'
# directory =r'C:\Users\Manish Kathane\PycharmProjects\Manish'
#
# import os
# image_path =r'IMG3.jpg'
# directory =r'C:\Users\Manish Kathane\OneDrive\Desktop' #C:\Users\Manish Kathane\PycharmProjects\Manish
# img = cv2.imread(image_path)
# os.chdir(directory)
# print("Before saving image:")
# print(os.listdir(directory))
# filename = 'savedImage.jpg';
# cv2.imwrite(filename, img)
# print("After saving image:")
# print(os.listdir(directory))
# print("Successfully saved image:")

# import cv2
# import numpy as np
# img1 = cv2.imread('I1.jpg')
# img2 = cv2.imread('I2.jpg')
# dest_or = cv2.bitwise_or(img2, img1, mask = None)
# cv2.imshow('Manish', dest_or)
#
# if cv2.waitKey(0) & 0xff == 27:
#     cv2.destroyAllWindows()


# import cv2
# import numpy as np
# img1 = cv2.imread("I1.jpg")
# img2 = cv2.imread("I2.jpg")
# dest_xor = cv2.bitwise_xor(img1, img2, mask = None)
# cv2.imshow("Manish", dest_xor)
#
# if cv2.waitKey(0) & 0xff == 27:
#    cv2.destroyAllWindows()


import cv2
import numpy as np

img1 = cv2.imread("I1.jpg")
img2 = cv2.imread("I2.jpg")
dest_not1 = cv2.bitwise_not(img1, mask = None)
dest_not2 = cv2.bitwise_not(img2, mask = None)
cv2.imshow("MANISH", dest_not1)
cv2.imshow("MANISH", dest_not2)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
