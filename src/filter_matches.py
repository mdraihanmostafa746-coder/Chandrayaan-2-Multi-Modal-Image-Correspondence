from pathlib import Path
import cv2


CROPS_DIR = Path("data/processed/crops")

MIN_GOOD_MATCHES = 10
RATIO_TEST_THRESHOLD = 0.75


def get_crop_dirs():
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


def calculate_matches(ohrc_path, tmc_path):
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

    orb = cv2.ORB_create(nfeatures=1500)

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

    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)

    knn_matches = matcher.knnMatch(
        descriptors1,
        descriptors2,
        k=2
    )

    good_matches = []

    for pair in knn_matches:
        if len(pair) < 2:
            continue

        first_match, second_match = pair

        if first_match.distance < (
            RATIO_TEST_THRESHOLD * second_match.distance
        ):
            good_matches.append(first_match)

    return len(keypoints1), len(keypoints2), good_matches


def main():
    ohrc_dirs, tmc_dirs = get_crop_dirs()

    if not ohrc_dirs or not tmc_dirs:
        print("Required OHRC/TMC crop directories not found.")
        return

    tmc_crops = sorted(tmc_dirs[0].glob("crop_*.png"))

    total_pairs = 0
    accepted_pairs = 0

    for ohrc_dir in ohrc_dirs:
        ohrc_crops = sorted(ohrc_dir.glob("crop_*.png"))

        for ohrc_crop in ohrc_crops:
            for tmc_crop in tmc_crops:
                result = calculate_matches(
                    ohrc_crop,
                    tmc_crop
                )

                if result is None:
                    continue

                keypoints1, keypoints2, good_matches = result

                total_pairs += 1

                if len(good_matches) >= MIN_GOOD_MATCHES:
                    accepted_pairs += 1
                    status = "Accepted"
                else:
                    status = "Rejected"

                print(
                    f"{ohrc_crop.parent.name}/{ohrc_crop.name} "
                    f"↔ {tmc_crop.name} | "
                    f"Keypoints: {keypoints1}/{keypoints2} | "
                    f"Good matches: {len(good_matches)} | "
                    f"{status}"
                )

    print("\nMatching quality filtering completed.")
    print(f"Total crop pairs: {total_pairs}")
    print(f"Accepted pairs: {accepted_pairs}")
    print(f"Rejected pairs: {total_pairs - accepted_pairs}")


if __name__ == "__main__":
    main()