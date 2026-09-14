from pathlib import Path

import cv2
import pandas as pd


CROP_DIR = Path("data/processed/crops")
OUTPUT_FILE = Path("results/scale_robustness.csv")

SCALES = [0.5, 0.75, 1.0, 1.5, 2.0]


def calculate_orb_score(image_1, image_2):
    orb = cv2.ORB_create(nfeatures=1000)

    keypoints_1, descriptors_1 = orb.detectAndCompute(image_1, None)
    keypoints_2, descriptors_2 = orb.detectAndCompute(image_2, None)

    if descriptors_1 is None or descriptors_2 is None:
        return len(keypoints_1), len(keypoints_2), 0, 0.0

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(descriptors_1, descriptors_2)

    good_matches = [
        match for match in matches
        if match.distance < 60
    ]

    score = len(good_matches) / max(len(matches), 1)

    return (
        len(keypoints_1),
        len(keypoints_2),
        len(good_matches),
        score,
    )


def main():
    image_1_path = CROP_DIR / "crop_000.png"
    image_2_path = CROP_DIR / "crop_001.png"

    image_1 = cv2.imread(str(image_1_path), cv2.IMREAD_GRAYSCALE)
    image_2 = cv2.imread(str(image_2_path), cv2.IMREAD_GRAYSCALE)

    if image_1 is None or image_2 is None:
        raise FileNotFoundError("Could not load crop_000.png or crop_001.png")

    results = []

    for scale in SCALES:
        new_width = int(image_2.shape[1] * scale)
        new_height = int(image_2.shape[0] * scale)

        scaled_image_2 = cv2.resize(
            image_2,
            (new_width, new_height),
            interpolation=cv2.INTER_LINEAR,
        )

        kp1, kp2, good_matches, score = calculate_orb_score(
            image_1,
            scaled_image_2,
        )

        results.append(
            {
                "scale": scale,
                "keypoints_image_1": kp1,
                "keypoints_scaled_image_2": kp2,
                "good_matches": good_matches,
                "matching_score": round(score, 4),
            }
        )

        print(
            f"Scale: {scale}x | "
            f"Keypoints: {kp1}/{kp2} | "
            f"Good matches: {good_matches} | "
            f"Score: {score:.4f}"
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(results).to_csv(OUTPUT_FILE, index=False)

    print(f"\nSaved results to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
