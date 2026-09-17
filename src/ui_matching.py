import cv2
import numpy as np


def run_orb_matching(image_1_bytes, image_2_bytes):

    image_1_array = np.frombuffer(image_1_bytes, np.uint8)
    image_2_array = np.frombuffer(image_2_bytes, np.uint8)

    image_1 = cv2.imdecode(
        image_1_array,
        cv2.IMREAD_GRAYSCALE
    )

    image_2 = cv2.imdecode(
        image_2_array,
        cv2.IMREAD_GRAYSCALE
    )

    if image_1 is None or image_2 is None:
        raise ValueError("Unable to read one or both images.")

    # Gaussian Blur preprocessing
    image_1_blur = cv2.GaussianBlur(
        image_1,
        (5, 5),
        0
    )

    image_2_blur = cv2.GaussianBlur(
        image_2,
        (5, 5),
        0
    )

    # ORB detector
    orb = cv2.ORB_create(
        nfeatures=1000
    )

    keypoints_1, descriptors_1 = orb.detectAndCompute(
        image_1_blur,
        None
    )

    keypoints_2, descriptors_2 = orb.detectAndCompute(
        image_2_blur,
        None
    )

    if descriptors_1 is None or descriptors_2 is None:
        raise ValueError("No features were detected in the images.")

    # BFMatcher with Hamming distance
    matcher = cv2.BFMatcher(
        cv2.NORM_HAMMING
    )

    matches = matcher.knnMatch(
        descriptors_1,
        descriptors_2,
        k=2
    )

    good_matches = []

    for pair in matches:

        if len(pair) == 2:

            first_match, second_match = pair

            if first_match.distance < 0.75 * second_match.distance:
                good_matches.append(first_match)

    matching_score = len(good_matches) / max(
        len(keypoints_1),
        len(keypoints_2),
        1
    )

    matched_image = cv2.drawMatches(
        image_1,
        keypoints_1,
        image_2,
        keypoints_2,
        good_matches,
        None,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )

    return {
        "keypoints_1": len(keypoints_1),
        "keypoints_2": len(keypoints_2),
        "good_matches": len(good_matches),
        "matching_score": matching_score,
        "matched_image": matched_image
    }