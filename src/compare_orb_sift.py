from pathlib import Path

import cv2
import pandas as pd


CROP_DIR = Path("data/processed/crops")
OUTPUT_FILE = Path("results/orb_vs_sift_comparison.csv")


def compare_pair(image_1_path: Path, image_2_path: Path) -> dict:
    image_1 = cv2.imread(str(image_1_path), cv2.IMREAD_GRAYSCALE)
    image_2 = cv2.imread(str(image_2_path), cv2.IMREAD_GRAYSCALE)

    if image_1 is None or image_2 is None:
        raise FileNotFoundError("Could not load one or both images.")

    # ORB
    orb = cv2.ORB_create(nfeatures=1000)

    orb_kp1, orb_des1 = orb.detectAndCompute(image_1, None)
    orb_kp2, orb_des2 = orb.detectAndCompute(image_2, None)

    orb_score = 0.0
    orb_good_matches = 0

    if orb_des1 is not None and orb_des2 is not None:
        orb_matcher = cv2.BFMatcher(
            cv2.NORM_HAMMING,
            crossCheck=True,
        )

        orb_matches = orb_matcher.match(orb_des1, orb_des2)
        orb_matches = sorted(orb_matches, key=lambda m: m.distance)

        orb_good_matches = sum(
            match.distance < 60 for match in orb_matches
        )

        orb_score = orb_good_matches / max(len(orb_matches), 1)

    # SIFT
    sift = cv2.SIFT_create(nfeatures=1000)

    sift_kp1, sift_des1 = sift.detectAndCompute(image_1, None)
    sift_kp2, sift_des2 = sift.detectAndCompute(image_2, None)

    sift_score = 0.0
    sift_good_matches = 0

    if sift_des1 is not None and sift_des2 is not None:
        sift_matcher = cv2.BFMatcher(cv2.NORM_L2)

        knn_matches = sift_matcher.knnMatch(
            sift_des1,
            sift_des2,
            k=2,
        )

        sift_good_matches = sum(
            first.distance < 0.75 * second.distance
            for first, second in knn_matches
            if len((first, second)) == 2
        )

        sift_score = sift_good_matches / max(len(knn_matches), 1)

    return {
        "image_1": image_1_path.name,
        "image_2": image_2_path.name,
        "orb_keypoints_1": len(orb_kp1),
        "orb_keypoints_2": len(orb_kp2),
        "orb_good_matches": orb_good_matches,
        "orb_score": round(orb_score, 4),
        "sift_keypoints_1": len(sift_kp1),
        "sift_keypoints_2": len(sift_kp2),
        "sift_good_matches": sift_good_matches,
        "sift_score": round(sift_score, 4),
        "better_method": "ORB" if orb_score >= sift_score else "SIFT",
    }


def main() -> None:
    crop_files = sorted(CROP_DIR.glob("*.png"))

    if len(crop_files) < 2:
        raise RuntimeError("At least two crop images are required.")

    rows = []

    for index in range(len(crop_files) - 1):
        rows.append(
            compare_pair(
                crop_files[index],
                crop_files[index + 1],
            )
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(OUTPUT_FILE, index=False)

    print("Comparison completed.")
    print("Total image pairs:", len(dataframe))
    print("ORB wins:", (dataframe["better_method"] == "ORB").sum())
    print("SIFT wins:", (dataframe["better_method"] == "SIFT").sum())
    print("Average ORB score:", round(dataframe["orb_score"].mean(), 4))
    print("Average SIFT score:", round(dataframe["sift_score"].mean(), 4))
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()