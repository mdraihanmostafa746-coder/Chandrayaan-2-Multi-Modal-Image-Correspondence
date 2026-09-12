import csv
from pathlib import Path
import cv2


CSV_PATH = Path("data/metadata/data-catalogue.csv")
RAW_DIR = Path("data/raw")


def find_image_file(file_name):
    matches = list(RAW_DIR.rglob(file_name))

    if matches:
        return matches[0]

    return None


def main():
    if not CSV_PATH.exists():
        print(f"CSV file not found: {CSV_PATH}")
        return

    if not RAW_DIR.exists():
        print(f"Raw data directory not found: {RAW_DIR}")
        return

    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    print(f"Total CSV records: {len(rows)}")
    print("-" * 60)

    found_count = 0
    missing_count = 0
    unreadable_count = 0

    for index, row in enumerate(rows, start=1):
        file_name = row.get("file_name", "").strip()
        instrument = row.get("instrument", "").strip()

        print(f"Record {index}: {file_name}")
        print(f"Instrument: {instrument}")

        image_path = find_image_file(file_name)

        if image_path is None:
            print("Status: FILE NOT FOUND")
            missing_count += 1
            print("-" * 60)
            continue

        print(f"Path: {image_path}")

        image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)

        if image is None:
            print("Status: FILE FOUND, BUT IMAGE CANNOT BE READ")
            unreadable_count += 1
        else:
            print(f"Status: OK")
            print(f"Actual image shape: {image.shape}")
            print(f"Data type: {image.dtype}")
            found_count += 1

        print("-" * 60)

    print("DATASET VALIDATION SUMMARY")
    print(f"Total records: {len(rows)}")
    print(f"Found and readable: {found_count}")
    print(f"Missing files: {missing_count}")
    print(f"Unreadable files: {unreadable_count}")


if __name__ == "__main__":
    main()