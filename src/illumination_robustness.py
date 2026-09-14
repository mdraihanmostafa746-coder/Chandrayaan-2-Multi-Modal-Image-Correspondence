from pathlib import Path

import cv2
import pandas as pd

CROP_DIR = Path("data/processed/crops")
OUTPUT_FILE = Path("results/illumination_robustness.csv")

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


def adjust_illumination(image, brightness, contrast, gamma):
    adjusted = cv2.convertScaleAbs(
        image,
        alpha=contrast,
        beta=brightness
    )

    normalized = adjusted / 255.0
    gamma_corrected = (normalized ** gamma) * 255
    gamma_corrected = gamma_corrected.astype("uint8")

    return gamma_corrected


image1 = cv2.imread(str(IMAGE_1), cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread(str(IMAGE_2), cv2.IMREAD_GRAYSCALE)

if image1 is None or image2 is None:
    raise FileNotFoundError("Crop images not found.")

settings = [
    ("normal", 0, 1.0, 1.0),
    ("bright", 40, 1.0, 1.0),
    ("dark", -40, 1.0, 1.0),
    ("high_contrast", 0, 1.5, 1.0),
    ("low_contrast", 0, 0.6, 1.0),
    ("gamma_bright", 0, 1.0, 0.6),
    ("gamma_dark", 0, 1.0, 1.8),
]

results = []

for name, brightness, contrast, gamma in settings:
    transformed = adjust_illumination(
        image2,
        brightness,
        contrast,
        gamma
    )

    kp1, kp2, good_matches, score = orb_score(image1, transformed)

    results.append({
        "condition": name,
        "brightness": brightness,
        "contrast": contrast,
        "gamma": gamma,
        "keypoints_image_1": kp1,
        "keypoints_image_2": kp2,
        "good_matches": good_matches,
        "matching_score": round(score, 4)
    })

    print(
        f"{name}: "
        f"keypoints=({kp1}, {kp2}), "
        f"good_matches={good_matches}, "
        f"score={score:.4f}"
    )

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df = pd.DataFrame(results)
df.to_csv(OUTPUT_FILE, index=False)

print(f"\nSaved: {OUTPUT_FILE}")
