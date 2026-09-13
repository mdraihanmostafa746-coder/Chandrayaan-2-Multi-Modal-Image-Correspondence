
from pathlib import Path

import cv2
import numpy as np


def create_overlapping_crops(
    image: np.ndarray,
    crop_size: tuple[int, int] = (256, 256),
    overlap: float = 0.25,
) -> list[np.ndarray]:
    """Create overlapping crops from a large image."""
    if not 0 <= overlap < 1:
        raise ValueError("Overlap must be between 0 and 1.")

    crop_height, crop_width = crop_size
    image_height, image_width = image.shape[:2]

    if crop_height > image_height or crop_width > image_width:
        raise ValueError("Crop size cannot exceed image size.")

    stride_y = max(1, int(crop_height * (1 - overlap)))
    stride_x = max(1, int(crop_width * (1 - overlap)))

    crops = []

    for y in range(0, image_height - crop_height + 1, stride_y):
        for x in range(0, image_width - crop_width + 1, stride_x):
            crop = image[
                y:y + crop_height,
                x:x + crop_width
            ]
            crops.append(crop.copy())

    return crops


def save_crops(
    crops: list[np.ndarray],
    output_dir: str = "data/processed/crops",
) -> None:
    """Save image crops to disk."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for index, crop in enumerate(crops):
        cv2.imwrite(
            str(output_path / f"crop_{index:03d}.png"),
            crop,
        )


if __name__ == "__main__":
    image_path = Path(
        "data/raw/ohrc/chandrayaan2_11_large copy.png.webp"
    )

    image = cv2.imread(str(image_path))

    if image is None:
        raise FileNotFoundError(f"Could not load: {image_path}")

    crops = create_overlapping_crops(image)

    save_crops(crops)

    print("Original image shape:", image.shape)
    print("Number of crops:", len(crops))
    print("Crop size:", crops[0].shape)
    print("Crops saved successfully!")