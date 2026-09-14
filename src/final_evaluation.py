from pathlib import Path

import pandas as pd

RESULT_DIR = Path("results")
OUTPUT_FILE = RESULT_DIR / "final_method_comparison.csv"

files = {
    "ORB": RESULT_DIR / "feature_matching.csv",
    "SIFT": RESULT_DIR / "sift_matching.csv",
    "ORB + CLAHE": RESULT_DIR / "improved_orb_clahe.csv",
    "ORB + Gaussian Blur": RESULT_DIR / "preprocessing_experiments.csv",
}

rows = []

for method, file_path in files.items():
    if not file_path.exists():
        print(f"Skipped missing file: {file_path}")
        continue

    df = pd.read_csv(file_path)

    if method == "ORB + Gaussian Blur":
        df = df[df["method"] == "gaussian_blur"]

    if df.empty:
        continue

    row = df.iloc[0].to_dict()
    row["method"] = method
    rows.append(row)

comparison = pd.DataFrame(rows)

if comparison.empty:
    raise ValueError("No result files found.")

comparison = comparison.sort_values(
    by="matching_score",
    ascending=False
)

RESULT_DIR.mkdir(parents=True, exist_ok=True)
comparison.to_csv(OUTPUT_FILE, index=False)

print("\nFinal Method Comparison:")
print(
    comparison[
        [
            "method",
            "keypoints_image_1",
            "keypoints_image_2",
            "good_matches",
            "matching_score",
        ]
    ].to_string(index=False)
)

best_method = comparison.iloc[0]["method"]
best_score = comparison.iloc[0]["matching_score"]

print(f"\nBest method: {best_method}")
print(f"Best matching score: {best_score:.4f}")
print(f"Saved: {OUTPUT_FILE}")
