from pathlib import Path
import cv2


CROPS_DIR = Path("data/processed/crops")
OUTPUT_DIR = Path("results/matching")


def load_images():
    image_dirs = sorted(
        path for path in CROPS_DIR.iterdir()
        if path.is_dir()
    )

    ohrc_dirs = [
        path for path in image_dirs
        if path.name.startswith("chandrayaan")
        or path.name.startswith("ohrc")
    ]

    tmc_dirs = [
        path for path in image_dirs
        if path.name.startswith("tmc")
    ]

    return ohrc_dirs, tmc_dirs


def match_images(ohrc_path, tmc_path):
    ohrc_image = cv2.imread(
        str(ohrc_path),
        cv2.IMREAD_GRAYSCALE
    )

    tmc_image = cv2.imread(
        str(tmc_path),
        cv2.IMREAD_GRAYSCALE
    )

    if ohrc_image is None or tmc_image is None:
        return None

    orb = cv2.ORB_create(nfeatures=1000)

    keypoints1, descriptors1 = orb.detectAndCompute(
        ohrc_image,
        None
    )

    keypoints2, descriptors2 = orb.detectAndCompute(
        tmc_image,
        None
    )

    if descriptors1 is None or descriptors2 is None:
        return None

    matcher = cv2.BFMatcher(
        cv2.NORM_HAMMING,
        crossCheck=True
    )

    matches = matcher.match(descriptors1, descriptors2)

    matches = sorted(
        matches,
        key=lambda match: match.distance
    )

    return matches, keypoints1, keypoints2


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    ohrc_dirs, tmc_dirs = load_images()

    if not ohrc_dirs:
        print("No OHRC crop directories found.")
        return

    if not tmc_dirs:
        print("No TMC crop directory found.")
        return

    tmc_crops = sorted(tmc_dirs[0].glob("crop_*.png"))

    total_matches = 0

    for ohrc_dir in ohrc_dirs:
        ohrc_crops = sorted(ohrc_dir.glob("crop_*.png"))

        for ohrc_crop in ohrc_crops:
            for tmc_crop in tmc_crops:
                result = match_images(ohrc_crop, tmc_crop)

                if result is None:
                    continue

                matches, keypoints1, keypoints2 = result

                total_matches += len(matches)

                print(
                    f"{ohrc_crop.name} ↔ "
                    f"{tmc_crop.name}: "
                    f"{len(matches)} matches"
                )

    print(f"\nTotal matches found: {total_matches}")


if __name__ == "__main__":
    main()