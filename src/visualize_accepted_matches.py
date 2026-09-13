from pathlib import Path

import cv2


CROPS_DIR = Path("data/processed/crops")
OUTPUT_DIR = Path("results/accepted_matches")

RATIO_TEST_THRESHOLD = 0.75
MIN_GOOD_MATCHES = 10
MAX_VISUALIZATIONS = 10


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


def find_good_matches(ohrc_path, tmc_path):
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

    good_matches = sorted(
        good_matches,
        key=lambda match: match.distance
    )

    return (
        ohrc_image,
        tmc_image,
        keypoints1,
        keypoints2,
        good_matches,
    )


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    ohrc_dirs, tmc_dirs = get_crop_dirs()

    if not ohrc_dirs or not tmc_dirs:
        print("OHRC/TMC crop directories not found.")
        return

    tmc_crops = sorted(tmc_dirs[0].glob("crop_*.png"))

    visualization_count = 0

    for ohrc_dir in ohrc_dirs:
        ohrc_crops = sorted(ohrc_dir.glob("crop_*.png"))

        for ohrc_crop in ohrc_crops:
            for tmc_crop in tmc_crops:
                if visualization_count >= MAX_VISUALIZATIONS:
                    break

                result = find_good_matches(
                    ohrc_crop,
                    tmc_crop
                )

                if result is None:
                    continue

                (
                    ohrc_image,
                    tmc_image,
                    keypoints1,
                    keypoints2,
                    good_matches,
                ) = result

                if len(good_matches) < MIN_GOOD_MATCHES:
                    continue

                selected_matches = good_matches[:30]

                output_image = cv2.drawMatches(
                    ohrc_image,
                    keypoints1,
                    tmc_image,
                    keypoints2,
                    selected_matches,
                    None,
                    flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
                )

                output_name = (
                    f"{ohrc_dir.name}_{ohrc_crop.stem}"
                    f"__{tmc_crop.stem}.png"
                )

                output_path = OUTPUT_DIR / output_name

                cv2.imwrite(
                    str(output_path),
                    output_image
                )

                visualization_count += 1

                print(
                    f"Saved: {output_path} | "
                    f"Good matches: {len(good_matches)}"
                )

            if visualization_count >= MAX_VISUALIZATIONS:
                break

        if visualization_count >= MAX_VISUALIZATIONS:
            break

    print(
        f"\nAccepted match visualizations created: "
        f"{visualization_count}"
    )


if __name__ == "__main__":
    main()