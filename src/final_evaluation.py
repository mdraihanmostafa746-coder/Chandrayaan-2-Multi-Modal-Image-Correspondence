from pathlib import Path

import pandas as pd

RESULT_DIR = Path("results")
OUTPUT_FILE = RESULT_DIR / "final_method_comparison.csv"

rows = []

# ORB and SIFT results from comparison file
comparison_file = RESULT_DIR / "orb_vs_sift_comparison.csv"

if comparison_file.exists():
    comparison = pd.read_csv(comparison_file)

    # Use the first crop pair for consistent comparison
    first_pair = comparison.iloc[0]

    rows.append({
        "method": "ORB",
        "keypoints_image_1": int(first_pair["orb_keypoints_1"]),
        "keypoints_image_2": int(first_pair["orb_keypoints_2"]),
        "good_matches": int(first_pair["orb_good_matches"]),
        "matching_score": float(first_pair["orb_score"])
    })

    rows.append({
        "method": "SIFT",
        "keypoints_image_1": int(first_pair["sift_keypoints_1"]),
        "keypoints_image_2": int(first_pair["sift_keypoints_2"]),
        "good_matches": int(first_pair["sift_good_matches"]),
        "matching_score": float(first_pair["sift_score"])
    })

# ORB + Gaussian Blur
preprocessing_file = RESULT_DIR / "preprocessing_experiments.csv"

if preprocessing_file.exists():
    preprocessing = pd.read_csv(preprocessing_file)
    gaussian = preprocessing[
        preprocessing["method"] == "gaussian_blur"
    ]

    if not gaussian.empty:
        row = gaussian.iloc[0]

        rows.append({
            "method": "ORB + Gaussian Blur",
            "keypoints_image_1": int(row["keypoints_image_1"]),
            "keypoints_image_2": int(row["keypoints_image_2"]),
            "good_matches": int(row["good_matches"]),
            "matching_score": float(row["matching_score"])
        })

# ORB + CLAHE
clahe_file = RESULT_DIR / "improved_orb_clahe.csv"

if clahe_file.exists():
    clahe = pd.read_csv(clahe_file)

    if not clahe.empty:
        row = clahe.iloc[0]

        rows.append({
            "method": "ORB + CLAHE",
            "keypoints_image_1": int(row["keypoints_image_1"]),
            "keypoints_image_2": int(row["keypoints_image_2"]),
            "good_matches": int(row["good_matches"]),
            "matching_score": float(row["matching_score"])
        })

if not rows:
    raise ValueError("No evaluation results found.")

result = pd.DataFrame(rows)
result = result.sort_values(
    by="matching_score",
    ascending=False
)

result.to_csv(OUTPUT_FILE, index=False)

print("\nFinal Method Comparison:")
print(result.to_string(index=False))

best_method = result.iloc[0]["method"]
best_score = result.iloc[0]["matching_score"]

print(f"\nBest method: {best_method}")
print(f"Best matching score: {best_score:.4f}")
print(f"Saved: {OUTPUT_FILE}")
