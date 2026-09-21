
from pathlib import Path

import cv2


def cross_sensor_match(
    image_path_1: str,
    image_path_2: str,
    output_path: str,
) -> None:
    """Compare feature matches between two sensor images."""

    image_1 = cv2.imread(image_path_1, cv2.IMREAD_GRAYSCALE)
    image_2 = cv2.imread(image_path_2, cv2.IMREAD_GRAYSCALE)

    if image_1 is None or image_2 is None:
        raise FileNotFoundError("Could not load sensor images.")

    orb = cv2.ORB_create(nfeatures=2000)

    keypoints_1, descriptors_1 = orb.detectAndCompute(
        image_1, None
    )
    keypoints_2, descriptors_2 = orb.detectAndCompute(
        image_2, None
    )

    if descriptors_1 is None or descriptors_2 is None:
        print("Not enough features found.")
        return

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)

    knn_matches = matcher.knnMatch(
        descriptors_1,
        descriptors_2,
        k=2,
    )

    good_matches = []

    for pair in knn_matches:
        if len(pair) < 2:
            continue

        best, second = pair

        if best.distance < 0.75 * second.distance:
            good_matches.append(best)

    good_matches = sorted(
        good_matches,
        key=lambda match: match.distance,
    )

    result = cv2.drawMatches(
        image_1,
        keypoints_1,
        image_2,
        keypoints_2,
        good_matches[:50],
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output), result)

    print("OHRC keypoints:", len(keypoints_1))
    print("TMC keypoints:", len(keypoints_2))
    print("Cross-sensor good matches:", len(good_matches))
    print("Saved:", output)


if __name__ == "__main__":
    cross_sensor_match(
        "data/raw/ohrc/chandrayaan2_11_large copy.png.webp",
        "data/raw/tmc/tmc-2-1_large.png.webp",
        "results/cross_sensor_matches.png",
    )