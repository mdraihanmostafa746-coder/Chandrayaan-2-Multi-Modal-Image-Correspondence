
from pathlib import Path

import cv2

from reliable_matching import reliable_match


def evaluate_pair(image_path_1, image_path_2, name):
    output_path = Path(f"results/{name}.png")

    ratio_count, inlier_count = reliable_match(
        str(image_path_1),
        str(image_path_2),
        str(output_path),
    )

    print(f"\n{name}")
    print("Ratio-test matches:", ratio_count)
    print("RANSAC inliers:", inlier_count)

    return ratio_count, inlier_count


if __name__ == "__main__":
    crop_dir = Path("data/processed/crops")

    positive_pair = (
        crop_dir / "crop_000.png",
        crop_dir / "crop_001.png",
    )

    negative_pair = (
        crop_dir / "crop_000.png",
        crop_dir / "crop_015.png",
    )

    evaluate_pair(
        positive_pair[0],
        positive_pair[1],
        "evaluation_positive",
    )

    evaluate_pair(
        negative_pair[0],
        negative_pair[1],
        "evaluation_negative",
    )