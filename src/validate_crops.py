from pathlib import Path
import csv
import cv2
import numpy as np


CROPS_DIR = Path("data/processed/crops")
OUTPUT_FILE = Path("results/crop_quality.csv")


def analyze_crop(crop_path):
    image = cv2.imread(str(crop_path), cv2.IMREAD_GRAYSCALE)

    if image is None:
        return {
            "filename": crop_path.name,
            "width": "",
            "height": "",
            "readable": False,
            "mean_pixel": "",
            "std_pixel": "",
            "low_intensity_ratio": "",
            "high_intensity_ratio": "",
            "status": "Unreadable",
        }

    height, width = image.shape

    mean_pixel = float(np.mean(image))
    std_pixel = float(np.std(image))

    low_intensity_ratio = float(np.mean(image <= 5))
    high_intensity_ratio = float(np.mean(image >= 250))

    if width == 256 and height == 256 and std_pixel >= 5:
        status = "Valid"
    elif width != 256 or height != 256:
        status = "Invalid Size"
    elif std_pixel < 5:
        status = "Low Information"
    else:
        status = "Review"

    return {
        "filename": crop_path.name,
        "width": width,
        "height": height,
        "readable": True,
        "mean_pixel": round(mean_pixel, 2),
        "std_pixel": round(std_pixel, 2),
        "low_intensity_ratio": round(low_intensity_ratio, 4),
        "high_intensity_ratio": round(high_intensity_ratio, 4),
        "status": status,
    }


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    crop_records = []

    image_dirs = sorted(
        path for path in CROPS_DIR.iterdir()
        if path.is_dir()
    )

    for image_dir in image_dirs:
        crop_files = sorted(image_dir.glob("crop_*.png"))

        for crop_path in crop_files:
            record = analyze_crop(crop_path)
            record["source_image"] = image_dir.name
            crop_records.append(record)

    fieldnames = [
        "source_image",
        "filename",
        "width",
        "height",
        "readable",
        "mean_pixel",
        "std_pixel",
        "low_intensity_ratio",
        "high_intensity_ratio",
        "status",
    ]

    with OUTPUT_FILE.open("w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(crop_records)

    valid_count = sum(
        record["status"] == "Valid"
        for record in crop_records
    )

    low_info_count = sum(
        record["status"] == "Low Information"
        for record in crop_records
    )

    print(f"Total crops checked: {len(crop_records)}")
    print(f"Valid crops: {valid_count}")
    print(f"Low-information crops: {low_info_count}")
    print(f"Saved report: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()