
from pathlib import Path

import cv2


def visualize_matches(
    image_path_1: str,
    image_path_2: str,
    output_path: str,
) -> None:
    """Draw ORB feature matches between two images."""
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
        raise ValueError("Not enough features found.")

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda m: m.distance)

    good_matches = matches[:50]

    result = cv2.drawMatches(
        image_1,
        keypoints_1,
        image_2,
        keypoints_2,
        good_matches,
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output), result)

    print("Total matches:", len(matches))
    print("Visualized matches:", len(good_matches))
    print("Saved visualization:", output)


if __name__ == "__main__":
    visualize_matches(
        "data/processed/crops/crop_000.png",
        "data/processed/crops/crop_001.png",
        "results/feature_matches.png",
    )