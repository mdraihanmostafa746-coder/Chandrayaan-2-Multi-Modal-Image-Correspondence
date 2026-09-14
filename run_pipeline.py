import subprocess
import sys

STEPS = [
    ("Dataset validation", ["src/validate_dataset.py"]),
    ("Batch preprocessing", ["src/batch_preprocess.py"]),
    ("Crop generation", ["src/crop_images.py"]),
    ("Feature matching", ["src/feature_matching.py"]),
    ("SIFT matching", ["src/sift_matching.py"]),
    ("AKAZE availability check", ["src/akaze_matching.py"]),
    ("RANSAC verification", ["src/ransac_matching.py"]),
    ("Matching evaluation", ["src/evaluate_matching.py"]),
    ("Scale robustness test", ["src/scale_robustness.py"]),
    ("Illumination robustness test", ["src/illumination_robustness.py"]),
    ("Preprocessing experiments", ["src/preprocessing_experiments.py"]),
    ("Improved ORB + CLAHE", ["src/improved_orb_clahe.py"]),
    ("Final method evaluation", ["src/final_evaluation.py"]),
]

for name, script in STEPS:
    print("\n" + "=" * 60)
    print(f"Running: {name}")
    print("=" * 60)

    result = subprocess.run([sys.executable, *script])

    if result.returncode != 0:
        print(f"\nFAILED: {name}")
        sys.exit(result.returncode)

print("\n" + "=" * 60)
print("FULL PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)
