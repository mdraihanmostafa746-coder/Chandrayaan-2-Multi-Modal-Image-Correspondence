import csv
from pathlib import Path

import cv2
import numpy as np


CSV_PATH = Path("data/metadata/data-catalogue.csv")
RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("results")
OUTPUT_FILE = OUTPUT_DIR / "image_statistics.csv"


def find_image_file(file_name):
    matches = list(RAW_DIR.rglob(file_name))

    if matches:
        return matches[0]

    return None


def calculate_statistics(image):
    if image is None:
        return None

    if len(image.shape) == 2:
        height, width = image.shape
        channels = 1
    else:
        height, width, channels = image.shape

    return {
        "actual_width": width,
        "actual_height": height,
        "channels": channels,
        "data_type": str(image.dtype),
        "min_pixel": int(np.min(image)),
        "max_pixel": int(np.max(image)),
        "mean_pixel": round(float(np.mean(image)), 4),
        "std_pixel": round(float(np.std(image)), 4),
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    statistics_rows = []

    for row in rows:
        file_name = row["file_name"]
        instrument = row["instrument"]

        image_path = find_image_file(file_name)

        if image_path is None:
            print(f"Skipping missing file: {file_name}")
            continue

        image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
        stats = calculate_statistics(image)

        if stats is None:
            print(f"Cannot read image: {file_name}")
            continue

        result = {
            "file_name": file_name,
            "instrument": instrument,
            "file_path": str(image_path),
            **stats,
        }

        statistics_rows.append(result)

        print(f"Processed: {file_name}")

    if statistics_rows:
        fieldnames = statistics_rows[0].keys()

        with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(statistics_rows)

        print("\nStatistics saved to:")
        print(OUTPUT_FILE)
        print(f"Total processed images: {len(statistics_rows)}")
    else:
        print("No image statistics generated.")


if __name__ == "__main__":
    main()