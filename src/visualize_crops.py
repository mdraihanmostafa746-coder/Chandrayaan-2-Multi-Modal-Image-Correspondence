from pathlib import Path

import cv2
import matplotlib.pyplot as plt


CROPS_DIR = Path("data/processed/crops")
OUTPUT_DIR = Path("results/crop_visualizations")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    image_dirs = sorted(
        path for path in CROPS_DIR.iterdir()
        if path.is_dir()
    )

    for image_dir in image_dirs:
        crop_files = sorted(image_dir.glob("crop_*.png"))

        if not crop_files:
            print(f"No crops found in: {image_dir}")
            continue

        figure, axes = plt.subplots(3, 3, figsize=(10, 10))
        axes = axes.ravel()

        for index, crop_path in enumerate(crop_files[:9]):
            crop = cv2.imread(str(crop_path), cv2.IMREAD_GRAYSCALE)

            if crop is None:
                axes[index].set_title("Unreadable")
                axes[index].axis("off")
                continue

            axes[index].imshow(crop, cmap="gray")
            axes[index].set_title(crop_path.name)
            axes[index].axis("off")

        figure.suptitle(image_dir.name)
        figure.tight_layout()

        output_path = OUTPUT_DIR / f"{image_dir.name}_crops.png"
        figure.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close(figure)

        print(f"Saved: {output_path}")

    print("\nCrop visualization completed.")


if __name__ == "__main__":
    main()