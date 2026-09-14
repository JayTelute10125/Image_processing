# import cv2
#
# # Read damaged image
# img = cv2.imread("I-2.jpg")
#
# if img is None:
#     print("Error: cat_damaged.png not found!")
#     exit()
#
# # Read predefined mask
# mask = cv2.imread("generated_mask.jpg", 0)
#
# if mask is None:
#     print("Error: cat_mask.png not found!")
#     exit()
#
# # Inpainting using Navier-Stokes method
# restored_ns = cv2.inpaint(
#     img,
#     mask,
#     3,
#     cv2.INPAINT_NS
# )
#
# # Save result
# cv2.imwrite("restored_ns.png", restored_ns)
#
# # Display
# cv2.imshow("Original Damaged Image || CS24091", img)
# cv2.imshow("Predefined Mask || CS24091", mask)
# cv2.imshow("Restored - Navier Stokes || CS24091", restored_ns)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# #3
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Step 1: Read damaged image
# damaged_img = cv2.imread("I-2.jpg")
#
# if damaged_img is None:
#     print("Error: cat_damaged.png not found!")
#     exit()
#
# # Step 2: Create mask automatically
# height, width = damaged_img.shape[:2]
#
# mask_auto = np.zeros(
#     (height, width, 3),
#     dtype=np.uint8
# )
#
# for i in range(height):
#     for j in range(width):
#         if damaged_img[i, j].sum() > 0:
#             mask_auto[i, j] = [0, 0, 0]
#         else:
#             mask_auto[i, j] = [255, 255, 255]
#
# # Convert mask to grayscale
# mask_auto_gray = cv2.cvtColor(
#     mask_auto,
#     cv2.COLOR_BGR2GRAY
# )
#
# # Step 3: Telea inpainting
# restored_telea = cv2.inpaint(
#     damaged_img,
#     mask_auto_gray,
#     3,
#     cv2.INPAINT_TELEA
# )
#
# # Step 4: Navier-Stokes inpainting
# mask_predefined = cv2.imread(
#     "generated_mask.jpg",
#     0
# )
#
# if mask_predefined is None:
#     print("Error: cat_mask.png not found!")
#     exit()
#
# restored_ns = cv2.inpaint(
#     damaged_img,
#     mask_predefined,
#     3,
#     cv2.INPAINT_NS
# )
#
# # Step 5: Display results
# images = [
#     damaged_img,
#     mask_auto_gray,
#     restored_telea,
#     restored_ns
# ]
#
# titles = [
#     "Original Damaged || CS24091",
#     "Generated Mask",
#     "Restored - Telea",
#     "Restored - Navier-Stokes"
# ]
#
# plt.figure(figsize=(12, 6))
#
# for i in range(4):
#
#     plt.subplot(2, 2, i + 1)
#
#     if len(images[i].shape) == 2:
#         plt.imshow(images[i], cmap="gray")
#     else:
#         plt.imshow(
#             cv2.cvtColor(
#                 images[i],
#                 cv2.COLOR_BGR2RGB
#             )
#         )
#
#     plt.title(titles[i])
#     plt.axis("off")
#
# plt.tight_layout()
# plt.show()

#4
# import cv2
# import matplotlib.pyplot as plt
#
# # Read Gaussian noisy image
# img = cv2.imread(
#     "noisy_gaussian.png",
#     0
# )
#
# if img is None:
#     print("Error: noisy_gaussian.png not found!")
#     exit()
#
# # Apply Gaussian Blur
# restored = cv2.GaussianBlur(
#     img,
#     (5, 5),
#     0
# )
#
# # Display
# plt.figure(figsize=(10, 5))
#
# plt.subplot(1, 2, 1)
# plt.imshow(img, cmap="gray")
# plt.title("Gaussian Noisy Image ||CS24070")
# plt.axis("off")
#
# plt.subplot(1, 2, 2)
# plt.imshow(restored, cmap="gray")
# plt.title("Restored - Gaussian Blur")
# plt.axis("off")
#
# plt.tight_layout()
# plt.show()

#5
# import cv2
# import matplotlib.pyplot as plt
#
# # Read noisy image
# img = cv2.imread(
#     "noisy_salt_pepper.png",
#     0
# )
#
# if img is None:
#     print("Error: noisy_salt_pepper.png not found!")
#     exit()
#
# # Apply Median Filter
# restored = cv2.medianBlur(
#     img,
#     5
# )
#
# # Display
# plt.figure(figsize=(10, 5))
#
# plt.subplot(1, 2, 1)
# plt.imshow(img, cmap="gray")
# plt.title("Salt & Pepper Noise || CS24070")
# plt.axis("off")
#
# plt.subplot(1, 2, 2)
# plt.imshow(restored, cmap="gray")
# plt.title("Restored - Median Filter || CS24070")
# plt.axis("off")
#
# plt.tight_layout()
# plt.show()

#6
# import cv2
# import matplotlib.pyplot as plt
#
# # Read noisy image
# img = cv2.imread(
#     "noisy_image.png",
#     0
# )
#
# if img is None:
#     print("Error: noisy_image.png not found!")
#     exit()
#
# # Apply Non-local Means Denoising
# restored = cv2.fastNlMeansDenoising(
#     img,
#     None,
#     30,
#     7,
#     21
# )
#
# # Display
# plt.figure(figsize=(10, 5))
#
# plt.subplot(1, 2, 1)
# plt.imshow(img, cmap="gray")
# plt.title("Noisy Image")
# plt.axis("off")
#
# plt.subplot(1, 2, 2)
# plt.imshow(restored, cmap="gray")
# plt.title("Restored - Non-local Means")
# plt.axis("off")
#
# plt.tight_layout()
# plt.show()

#7
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Read scratched image
# img = cv2.imread(
#     "scratched.png",
#     0
# )
#
# if img is None:
#     print("Error: scratched.png not found!")
#     exit()
#
# # Create mask
# mask = np.zeros(
#     img.shape,
#     np.uint8
# )
#
# # Mark damaged region as white
# mask[50:80, 50:150] = 255
#
# # Inpaint damaged region
# restored = cv2.inpaint(
#     img,
#     mask,
#     3,
#     cv2.INPAINT_TELEA
# )
#
# # Display
# plt.figure(figsize=(12, 4))
#
# plt.subplot(1, 3, 1)
# plt.imshow(img, cmap="gray")
# plt.title("Damaged Image")
# plt.axis("off")
#
# plt.subplot(1, 3, 2)
# plt.imshow(mask, cmap="gray")
# plt.title("Mask")
# plt.axis("off")
#
# plt.subplot(1, 3, 3)
# plt.imshow(restored, cmap="gray")
# plt.title("Restored Image")
# plt.axis("off")
#
# plt.tight_layout()
# plt.show()

#11
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Create base image
img = np.ones(
    (256, 256),
    dtype=np.uint8
) * 200

# Add text
cv2.putText(
    img,
    "CAT",
    (70, 140),
    cv2.FONT_HERSHEY_SIMPLEX,
    2,
    50,
    5
)

# Copy image
scratched = img.copy()

# Add scratches
cv2.line(
    scratched,
    (30, 100),
    (220, 120),
    0,
    3
)

cv2.line(
    scratched,
    (100, 30),
    (120, 220),
    0,
    3
)

# Save scratched image
cv2.imwrite(
    "scratched.png",
    scratched
)

# Display
plt.imshow(
    scratched,
    cmap="gray"
)

plt.title("Scratched Image")
plt.axis("off")
plt.show()
