from pathlib import Path

import cv2
import pandas as pd

CROP_DIR = Path("data/processed/crops")
OUTPUT_FILE = Path("results/improved_orb_clahe.csv")

IMAGE_1 = CROP_DIR / "crop_000.png"
IMAGE_2 = CROP_DIR / "crop_001.png"


def apply_clahe(image):
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )
    return clahe.apply(image)


def main():
    image1 = cv2.imread(str(IMAGE_1), cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(str(IMAGE_2), cv2.IMREAD_GRAYSCALE)

    if image1 is None or image2 is None:
        raise FileNotFoundError("Crop images not found.")

    image1 = apply_clahe(image1)
    image2 = apply_clahe(image2)

    orb = cv2.ORB_create(
        nfeatures=2000,
        scaleFactor=1.2,
        nlevels=8
    )

    kp1, des1 = orb.detectAndCompute(image1, None)
    kp2, des2 = orb.detectAndCompute(image2, None)

    if des1 is None or des2 is None:
        raise ValueError("Descriptors could not be generated.")

    matcher = cv2.BFMatcher(
        cv2.NORM_HAMMING,
        crossCheck=True
    )

    matches = matcher.match(des1, des2)
    matches = sorted(matches, key=lambda m: m.distance)

    good_matches = [
        match for match in matches
        if match.distance < 60
    ]

    inliers = 0

    if len(good_matches) >= 4:
        points1 = cv2.UMat(
            __import__("numpy").float32(
                [kp1[m.queryIdx].pt for m in good_matches]
            )
        ).get()

        points2 = cv2.UMat(
            __import__("numpy").float32(
                [kp2[m.trainIdx].pt for m in good_matches]
            )
        ).get()

        _, mask = cv2.findHomography(
            points1,
            points2,
            cv2.RANSAC,
            5.0
        )

        if mask is not None:
            inliers = int(mask.sum())

    matching_score = len(good_matches) / max(len(matches), 1)
    inlier_ratio = inliers / max(len(good_matches), 1)

    result = pd.DataFrame([{
        "method": "Improved ORB + CLAHE",
        "keypoints_image_1": len(kp1),
        "keypoints_image_2": len(kp2),
        "total_matches": len(matches),
        "good_matches": len(good_matches),
        "ransac_inliers": inliers,
        "matching_score": round(matching_score, 4),
        "inlier_ratio": round(inlier_ratio, 4)
    }])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_FILE, index=False)

    print(f"Keypoints image 1: {len(kp1)}")
    print(f"Keypoints image 2: {len(kp2)}")
    print(f"Total matches: {len(matches)}")
    print(f"Good matches: {len(good_matches)}")
    print(f"RANSAC inliers: {inliers}")
    print(f"Matching score: {matching_score:.4f}")
    print(f"Inlier ratio: {inlier_ratio:.4f}")
    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
