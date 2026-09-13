from pathlib import Path

import cv2


INPUT_DIR = Path("data/processed/images")
OUTPUT_DIR = Path("data/processed/crops")

CROP_SIZE = 256
OVERLAP = 0.25
STEP = int(CROP_SIZE * (1 - OVERLAP))


def create_crops(image, crop_size, step):
    height, width = image.shape[:2]
    crops = []

    y_positions = list(range(0, max(height - crop_size, 0) + 1, step))
    x_positions = list(range(0, max(width - crop_size, 0) + 1, step))

    if not y_positions or y_positions[-1] + crop_size < height:
        y_positions.append(max(height - crop_size, 0))

    if not x_positions or x_positions[-1] + crop_size < width:
        x_positions.append(max(width - crop_size, 0))

    for y in sorted(set(y_positions)):
        for x in sorted(set(x_positions)):
            crop = image[y:y + crop_size, x:x + crop_size]

            if crop.shape[0] == crop_size and crop.shape[1] == crop_size:
                crops.append((x, y, crop))

    return crops


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    image_files = sorted(INPUT_DIR.glob("*_grayscale.png"))

    if not image_files:
        print("No grayscale images found.")
        return

    total_crops = 0

    for image_path in image_files:
        image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)

        if image is None:
            print(f"Could not read: {image_path.name}")
            continue

        crops = create_crops(image, CROP_SIZE, STEP)

        image_output_dir = OUTPUT_DIR / image_path.stem
        image_output_dir.mkdir(parents=True, exist_ok=True)

        for crop_index, (x, y, crop) in enumerate(crops):
            output_path = image_output_dir / f"crop_{crop_index:03d}_x{x}_y{y}.png"
            cv2.imwrite(str(output_path), crop)

        print(f"{image_path.name}: {len(crops)} crops created")
        total_crops += len(crops)

    print("\nCROP GENERATION SUMMARY")
    print(f"Total crops: {total_crops}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()