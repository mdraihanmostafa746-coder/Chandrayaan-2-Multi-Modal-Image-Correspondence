from pathlib import Path

import cv2
import pandas as pd

CROP_DIR = Path("data/processed/crops")
OUTPUT_FILE = Path("results/akaze_matching.csv")

IMAGE_1 = CROP_DIR / "crop_000.png"
IMAGE_2 = CROP_DIR / "crop_001.png"

image1 = cv2.imread(str(IMAGE_1), cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread(str(IMAGE_2), cv2.IMREAD_GRAYSCALE)

if image1 is None or image2 is None:
    raise FileNotFoundError("Crop images not found.")

if not hasattr(cv2, "AKAZE_create"):
    print("AKAZE is not available in this OpenCV installation.")
    print("AKAZE baseline skipped.")
    print("Use ORB and SIFT results for comparison.")
    raise SystemExit(0)

akaze = cv2.AKAZE_create()

kp1, des1 = akaze.detectAndCompute(image1, None)
kp2, des2 = akaze.detectAndCompute(image2, None)

if des1 is None or des2 is None:
    raise ValueError("Descriptors could not be generated.")

matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = matcher.match(des1, des2)

good_matches = [m for m in matches if m.distance < 60]
matching_score = len(good_matches) / max(len(matches), 1)

result = pd.DataFrame([{
    "method": "AKAZE",
    "keypoints_image_1": len(kp1),
    "keypoints_image_2": len(kp2),
    "total_matches": len(matches),
    "good_matches": len(good_matches),
    "matching_score": round(matching_score, 4)
}])

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT_FILE, index=False)

print(f"AKAZE keypoints in image 1: {len(kp1)}")
print(f"AKAZE keypoints in image 2: {len(kp2)}")
print(f"AKAZE total matches: {len(matches)}")
print(f"AKAZE good matches: {len(good_matches)}")
print(f"AKAZE matching score: {matching_score:.4f}")
print(f"Saved: {OUTPUT_FILE}")
