import subprocess
import sys

STEPS = [
    ("Dataset validation", ["src/validate_dataset.py"]),
    ("Batch preprocessing", ["src/batch_preprocess.py"]),
    ("Crop generation", ["src/crop_images.py"]),
    ("Feature matching", ["src/feature_matching.py"]),
    ("RANSAC verification", ["src/ransac_matching.py"]),
    ("Matching evaluation", ["src/evaluate_matching.py"]),
]

for name, script in STEPS:
    print(f"\n{'=' * 60}")
    print(f"Running: {name}")
    print(f"{'=' * 60}")

    result = subprocess.run([sys.executable, *script])

    if result.returncode != 0:
        print(f"\nFAILED: {name}")
        sys.exit(result.returncode)

print("\n" + "=" * 60)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)