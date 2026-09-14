from pathlib import Path

import cv2
import pandas as pd

CROP_DIR = Path("data/processed/crops")
OUTPUT_FILE = Path("results/preprocessing_experiments.csv")

IMAGE_1 = CROP_DIR / "crop_000.png"
IMAGE_2 = CROP_DIR / "crop_001.png"


def orb_score(image1, image2):
    orb = cv2.ORB_create(nfeatures=1000)

    kp1, des1 = orb.detectAndCompute(image1, None)
    kp2, des2 = orb.detectAndCompute(image2, None)

    if des1 is None or des2 is None:
        return len(kp1), len(kp2), 0, 0.0

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = matcher.match(des1, des2)

    good_matches = [m for m in matches if m.distance < 60]
    score = len(good_matches) / max(len(matches), 1)

    return len(kp1), len(kp2), len(good_matches), score


def preprocess(image, method):
    if method == "original":
        return image

    if method == "clahe":
        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )
        return clahe.apply(image)

    if method == "histogram_equalization":
        return cv2.equalizeHist(image)

    if method == "gaussian_blur":
        return cv2.GaussianBlur(image, (5, 5), 0)

    if method == "normalization":
        return cv2.normalize(
            image,
            None,
            alpha=0,
            beta=255,
            norm_type=cv2.NORM_MINMAX
        )

    raise ValueError(f"Unknown method: {method}")


image1 = cv2.imread(str(IMAGE_1), cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread(str(IMAGE_2), cv2.IMREAD_GRAYSCALE)

if image1 is None or image2 is None:
    raise FileNotFoundError("Crop images not found.")

methods = [
    "original",
    "clahe",
    "histogram_equalization",
    "gaussian_blur",
    "normalization",
]

results = []

for method in methods:
    processed1 = preprocess(image1, method)
    processed2 = preprocess(image2, method)

    kp1, kp2, good_matches, score = orb_score(
        processed1,
        processed2
    )

    results.append({
        "method": method,
        "keypoints_image_1": kp1,
        "keypoints_image_2": kp2,
        "good_matches": good_matches,
        "matching_score": round(score, 4)
    })

    print(
        f"{method}: "
        f"keypoints=({kp1}, {kp2}), "
        f"good_matches={good_matches}, "
        f"score={score:.4f}"
    )

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(results)
df.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved: {OUTPUT_FILE}")
