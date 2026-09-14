
from pathlib import Path

import cv2


def match_sift_features(
    image_path_1: str,
    image_path_2: str,
) -> tuple[int, int, float]:
    """Match SIFT features between two images."""

    image_1 = cv2.imread(image_path_1, cv2.IMREAD_GRAYSCALE)
    image_2 = cv2.imread(image_path_2, cv2.IMREAD_GRAYSCALE)

    if image_1 is None or image_2 is None:
        raise FileNotFoundError("Could not load one or both images.")

    sift = cv2.SIFT_create(nfeatures=1000)

    keypoints_1, descriptors_1 = sift.detectAndCompute(image_1, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(image_2, None)

    if descriptors_1 is None or descriptors_2 is None:
        return len(keypoints_1), len(keypoints_2), 0.0

    matcher = cv2.BFMatcher(cv2.NORM_L2)

    knn_matches = matcher.knnMatch(
        descriptors_1,
        descriptors_2,
        k=2,
    )

    good_matches = []

    for match_pair in knn_matches:
        if len(match_pair) == 2:
            match_1, match_2 = match_pair

            if match_1.distance < 0.75 * match_2.distance:
                good_matches.append(match_1)

    score = len(good_matches) / max(len(knn_matches), 1)

    return len(keypoints_1), len(keypoints_2), score


if __name__ == "__main__":
    crop_dir = Path("data/processed/crops")

    image_1 = crop_dir / "crop_000.png"
    image_2 = crop_dir / "crop_001.png"

    kp1, kp2, score = match_sift_features(
        str(image_1),
        str(image_2),
    )

    print("SIFT keypoints in image 1:", kp1)
    print("SIFT keypoints in image 2:", kp2)
    print("SIFT matching score:", round(score, 4))