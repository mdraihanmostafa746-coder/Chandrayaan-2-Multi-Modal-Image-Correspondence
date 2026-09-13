from pathlib import Path

import numpy as np

from preprocess import preprocess_image


IMAGE_PATH = Path(
    "data/raw/ohrc/chandrayaan2_11_large copy.png.webp"
)


image = preprocess_image(str(IMAGE_PATH))

print("Processed image shape:", image.shape)
print("Data type:", image.dtype)
print("Minimum value:", image.min())
print("Maximum value:", image.max())

assert isinstance(image, np.ndarray)
assert image.shape == (512, 512, 3)
assert image.dtype == np.float32
assert 0.0 <= image.min() <= image.max() <= 1.0

print("Preprocessing test passed!")