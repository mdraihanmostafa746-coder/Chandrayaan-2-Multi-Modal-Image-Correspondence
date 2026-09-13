from pathlib import Path
import csv

import cv2
import matplotlib.pyplot as plt


CSV_PATH = Path("data/metadata/data-catalogue.csv")
RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("results/dataset_visualizations")


def find_image_file(file_name):
    matches = list(RAW_DIR.rglob(file_name))

    if matches:
        return matches[0]

    return None


def safe_name(file_name):
    return Path(file_name).stem.replace(" ", "_")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))

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

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(grayscale, 100, 200)

        figure, axes = plt.subplots(2, 2, figsize=(12, 9))

        axes[0, 0].imshow(image_rgb)
        axes[0, 0].set_title("Original Image")
        axes[0, 0].axis("off")

        axes[0, 1].imshow(grayscale, cmap="gray")
        axes[0, 1].set_title("Grayscale Image")
        axes[0, 1].axis("off")

        axes[1, 0].hist(grayscale.ravel(), bins=256, range=(0, 256))
        axes[1, 0].set_title("Grayscale Pixel Histogram")
        axes[1, 0].set_xlabel("Pixel Intensity")
        axes[1, 0].set_ylabel("Frequency")

        axes[1, 1].imshow(edges, cmap="gray")
        axes[1, 1].set_title("Canny Edge Map")
        axes[1, 1].axis("off")

        figure.suptitle(f"{row['instrument']} - {file_name}")
        figure.tight_layout()

        output_path = OUTPUT_DIR / f"{safe_name(file_name)}_visualization.png"
        figure.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(figure)

        print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()