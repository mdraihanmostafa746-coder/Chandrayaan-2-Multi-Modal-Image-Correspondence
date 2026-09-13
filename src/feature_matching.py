
from pathlib import Path

import cv2


def match_features(
    image_path_1: str,
    image_path_2: str,
) -> tuple[int, int, float]:
    """Match ORB features between two images."""
    image_1 = cv2.imread(image_path_1, cv2.IMREAD_GRAYSCALE)
    image_2 = cv2.imread(image_path_2, cv2.IMREAD_GRAYSCALE)

    if image_1 is None or image_2 is None:
        raise FileNotFoundError("Could not load one or both images.")

    orb = cv2.ORB_create(nfeatures=1000)

    keypoints_1, descriptors_1 = orb.detectAndCompute(
        image_1, None
    )
    keypoints_2, descriptors_2 = orb.detectAndCompute(
        image_2, None
    )

    if descriptors_1 is None or descriptors_2 is None:
        return len(keypoints_1), len(keypoints_2), 0.0

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(descriptors_1, descriptors_2)

    matches = sorted(matches, key=lambda m: m.distance)

    good_matches = [
        match for match in matches
        if match.distance < 60
    ]

    score = len(good_matches) / max(len(matches), 1)

    return len(keypoints_1), len(keypoints_2), score


if __name__ == "__main__":
    crop_dir = Path("data/processed/crops")

    image_1 = crop_dir / "crop_000.png"
    image_2 = crop_dir / "crop_001.png"

    kp1, kp2, score = match_features(
        str(image_1),
        str(image_2),
    )

    print("Keypoints in image 1:", kp1)
    print("Keypoints in image 2:", kp2)
    print("Matching score:", round(score, 4))