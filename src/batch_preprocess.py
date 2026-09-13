from pathlib import Path
import csv

import cv2
import numpy as np


CSV_PATH = Path("data/metadata/data-catalogue.csv")
RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed/images")

TARGET_SIZE = (512, 512)


def find_image_file(file_name):
    matches = list(RAW_DIR.rglob(file_name))

    if matches:
        return matches[0]

    return None


def safe_name(file_name):
    return Path(file_name).stem.replace(" ", "_")


def preprocess_image(image):
    resized = cv2.resize(image, TARGET_SIZE)

    grayscale = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    normalized = cv2.normalize(
        grayscale,
        None,
        alpha=0,
        beta=255,
        norm_type=cv2.NORM_MINMAX,
    )

    return resized, grayscale, normalized


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

    processed_count = 0

    for row in rows:
        file_name = row["file_name"]
        image_path = find_image_file(file_name)

        if image_path is None:
            print(f"Skipping missing image: {file_name}")
            continue

        image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)

        if image is None:
            print(f"Cannot read image: {file_name}")
            continue

        resized, grayscale, normalized = preprocess_image(image)

        name = safe_name(file_name)

        cv2.imwrite(
            str(OUTPUT_DIR / f"{name}_resized.png"),
            resized,
        )

        cv2.imwrite(
            str(OUTPUT_DIR / f"{name}_grayscale.png"),
            grayscale,
        )

        cv2.imwrite(
            str(OUTPUT_DIR / f"{name}_normalized.png"),
            normalized,
        )

        processed_count += 1
        print(f"Processed: {file_name}")

    print("\nPREPROCESSING SUMMARY")
    print(f"Total processed images: {processed_count}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()