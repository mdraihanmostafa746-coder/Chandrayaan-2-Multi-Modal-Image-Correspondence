from pathlib import Path

import cv2

from crop_images import create_overlapping_crops
from reliable_matching import reliable_match


IMAGE_PATH = Path(
    "data/raw/ohrc/chandrayaan2_11_large copy.png.webp"
)


def main():
    image = cv2.imread(str(IMAGE_PATH))

    if image is None:
        raise FileNotFoundError("Image not found.")

    crops = create_overlapping_crops(
        image,
        crop_size=(256, 256),
        overlap=0.25,
    )

    test_dir = Path("data/processed/test_pairs")
    test_dir.mkdir(parents=True, exist_ok=True)

    cv2.imwrite(str(test_dir / "crop_a.png"), crops[0])
    cv2.imwrite(str(test_dir / "crop_b.png"), crops[1])

    print("Created test pair.")
    print("Crop A:", crops[0].shape)
    print("Crop B:", crops[1].shape)

    reliable_match(
        str(test_dir / "crop_a.png"),
        str(test_dir / "crop_b.png"),
        "results/test_pair_matches.png",
    )


if __name__ == "__main__":
    main()