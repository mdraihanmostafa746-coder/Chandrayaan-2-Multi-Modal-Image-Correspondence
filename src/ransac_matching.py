from pathlib import Path

import cv2
import numpy as np


CROPS_DIR = Path("data/processed/crops")
OUTPUT_DIR = Path("results/ransac_matches")

RATIO_TEST_THRESHOLD = 0.75
MIN_GOOD_MATCHES = 8
MIN_INLIERS = 6


def get_crop_dirs():
    image_dirs = sorted(
        path for path in CROPS_DIR.iterdir()
        if path.is_dir()
    )

    ohrc_dirs = [
        path for path in image_dirs
        if path.name.startswith("chandrayaan")
        or path.name.startswith("ohrc")
    ]

    tmc_dirs = [
        path for path in image_dirs
        if path.name.startswith("tmc")
    ]

    return ohrc_dirs, tmc_dirs


def calculate_ransac_matches(ohrc_path, tmc_path):
    ohrc_image = cv2.imread(
        str(ohrc_path),
        cv2.IMREAD_GRAYSCALE
    )

    tmc_image = cv2.imread(
        str(tmc_path),
        cv2.IMREAD_GRAYSCALE
    )

    if ohrc_image is None or tmc_image is None:
        return None

    orb = cv2.ORB_create(nfeatures=2000)

    keypoints1, descriptors1 = orb.detectAndCompute(
        ohrc_image,
        None
    )

    keypoints2, descriptors2 = orb.detectAndCompute(
        tmc_image,
        None
    )

    if descriptors1 is None or descriptors2 is None:
        return None

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)

    knn_matches = matcher.knnMatch(
        descriptors1,
        descriptors2,
        k=2
    )

    good_matches = []

    for pair in knn_matches:
        if len(pair) < 2:
            continue

        first_match, second_match = pair

        if first_match.distance < (
            RATIO_TEST_THRESHOLD * second_match.distance
        ):
            good_matches.append(first_match)

    if len(good_matches) < MIN_GOOD_MATCHES:
        return {
            "good_matches": good_matches,
            "inlier_matches": [],
            "keypoints1": keypoints1,
            "keypoints2": keypoints2,
            "image1": ohrc_image,
            "image2": tmc_image,
        }

    source_points = np.float32([
        keypoints1[match.queryIdx].pt
        for match in good_matches
    ]).reshape(-1, 1, 2)

    destination_points = np.float32([
        keypoints2[match.trainIdx].pt
        for match in good_matches
    ]).reshape(-1, 1, 2)

    homography, mask = cv2.findHomography(
        source_points,
        destination_points,
        cv2.RANSAC,
        5.0
    )

    if mask is None:
        inlier_matches = []
    else:
        inlier_matches = [
            match
            for match, flag in zip(good_matches, mask.ravel())
            if flag == 1
        ]

    return {
        "good_matches": good_matches,
        "inlier_matches": inlier_matches,
        "keypoints1": keypoints1,
        "keypoints2": keypoints2,
        "image1": ohrc_image,
        "image2": tmc_image,
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    ohrc_dirs, tmc_dirs = get_crop_dirs()

    if not ohrc_dirs or not tmc_dirs:
        print("OHRC/TMC crop directories not found.")
        return

    tmc_crops = sorted(tmc_dirs[0].glob("crop_*.png"))

    total_pairs = 0
    reliable_pairs = 0

    for ohrc_dir in ohrc_dirs:
        ohrc_crops = sorted(ohrc_dir.glob("crop_*.png"))

        for ohrc_crop in ohrc_crops:
            for tmc_crop in tmc_crops:
                result = calculate_ransac_matches(
                    ohrc_crop,
                    tmc_crop
                )

                if result is None:
                    continue

                total_pairs += 1

                good_matches = result["good_matches"]
                inlier_matches = result["inlier_matches"]

                inlier_count = len(inlier_matches)

                if inlier_count >= MIN_INLIERS:
                    reliable_pairs += 1
                    status = "Reliable"
                else:
                    status = "Unreliable"

                print(
                    f"{ohrc_crop.parent.name}/{ohrc_crop.name} "
                    f"<-> {tmc_crop.name} | "
                    f"Good: {len(good_matches)} | "
                    f"Inliers: {inlier_count} | "
                    f"{status}"
                )

                if status == "Reliable":
                    output_image = cv2.drawMatches(
                        result["image1"],
                        result["keypoints1"],
                        result["image2"],
                        result["keypoints2"],
                        inlier_matches[:30],
                        None,
                        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
                    )

                    output_name = (
                        f"{ohrc_dir.name}_{ohrc_crop.stem}"
                        f"__{tmc_crop.stem}_ransac.png"
                    )

                    output_path = OUTPUT_DIR / output_name

                    cv2.imwrite(
                        str(output_path),
                        output_image
                    )

    print("\nRANSAC matching completed.")
    print(f"Total pairs checked: {total_pairs}")
    print(f"Reliable pairs: {reliable_pairs}")
    print(f"Unreliable pairs: {total_pairs - reliable_pairs}")


if __name__ == "__main__":
    main()