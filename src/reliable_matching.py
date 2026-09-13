from pathlib import Path

import cv2
import numpy as np


def reliable_match(
    image_path_1: str,
    image_path_2: str,
    output_path: str,
) -> tuple[int, int]:
    image_1 = cv2.imread(image_path_1, cv2.IMREAD_GRAYSCALE)
    image_2 = cv2.imread(image_path_2, cv2.IMREAD_GRAYSCALE)

    if image_1 is None or image_2 is None:
        raise FileNotFoundError("Could not load images.")

    orb = cv2.ORB_create(nfeatures=2000)

    keypoints_1, descriptors_1 = orb.detectAndCompute(
        image_1, None
    )
    keypoints_2, descriptors_2 = orb.detectAndCompute(
        image_2, None
    )

    if descriptors_1 is None or descriptors_2 is None:
        print("Not enough features.")
        return 0, 0

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)

    knn_matches = matcher.knnMatch(
        descriptors_1,
        descriptors_2,
        k=2,
    )

    ratio_matches = []

    for pair in knn_matches:
        if len(pair) < 2:
            continue

        best, second = pair

        if best.distance < 0.75 * second.distance:
            ratio_matches.append(best)

    inlier_matches = ratio_matches

    if len(ratio_matches) >= 4:
        points_1 = np.float32([
            keypoints_1[m.queryIdx].pt
            for m in ratio_matches
        ])

        points_2 = np.float32([
            keypoints_2[m.trainIdx].pt
            for m in ratio_matches
        ])

        _, mask = cv2.findHomography(
            points_1,
            points_2,
            cv2.RANSAC,
            5.0,
        )

        if mask is not None:
            inlier_matches = [
                match
                for match, keep in zip(ratio_matches, mask.ravel())
                if keep
            ]

    result = cv2.drawMatches(
        image_1,
        keypoints_1,
        image_2,
        keypoints_2,
        inlier_matches,
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output), result)

    print("Keypoints image 1:", len(keypoints_1))
    print("Keypoints image 2:", len(keypoints_2))
    print("Ratio-test matches:", len(ratio_matches))
    print("RANSAC inlier matches:", len(inlier_matches))
    print("Saved:", output)

    return len(ratio_matches), len(inlier_matches)


if __name__ == "__main__":
    reliable_match(
        "data/processed/crops/crop_000.png",
        "data/processed/crops/crop_001.png",
        "results/reliable_matches.png",
    )