from pathlib import Path

import cv2
import numpy as np


def load_image(image_path: str) -> np.ndarray:
    """Load an image from disk."""
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Could not load image: {image_path}"
        )

    return image


def resize_image(
    image: np.ndarray,
    size: tuple[int, int] = (512, 512),
) -> np.ndarray:
    """Resize image to the target size."""
    return cv2.resize(image, size)


def normalize_image(image: np.ndarray) -> np.ndarray:
    """Normalize pixel values to the range 0-1."""
    return image.astype(np.float32) / 255.0


def preprocess_image(
    image_path: str,
    size: tuple[int, int] = (512, 512),
) -> np.ndarray:
    """Load, resize, and normalize an image."""
    image = load_image(image_path)
    image = resize_image(image, size)
    image = normalize_image(image)

    return image