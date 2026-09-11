from pathlib import Path

import cv2
import matplotlib.pyplot as plt


image_path = "data/raw/ohrc/chandrayaan2_11_large copy.png.webp"

image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)

if image is None:
    raise FileNotFoundError(f"Image not found or could not be opened: {image_path}")

print("Image shape:", image.shape)
print("Data type:", image.dtype)
print("Minimum value:", image.min())
print("Maximum value:", image.max())

plt.figure(figsize=(10, 8))

if len(image.shape) == 2:
    plt.imshow(image, cmap="gray")
else:
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)

plt.title("OHRC Image Inspection")
plt.axis("off")
plt.show()

