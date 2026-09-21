# ORB Feature Detection and Matching

## 1. Overview

ORB (Oriented FAST and Rotated BRIEF) is used as one of the classical baseline methods for detecting and matching local features between satellite image regions.

The purpose of this stage is to identify distinctive visual features and establish candidate correspondences between two image crops.

---

## 2. Objective

The main objectives of the ORB stage are:

- Detect distinctive keypoints
- Generate feature descriptors
- Match descriptors between two image regions
- Identify reliable candidate correspondences
- Provide matches for subsequent geometric verification using RANSAC

---

## 3. ORB Pipeline

The ORB-based matching pipeline follows:

```text
Image 1
   ↓
ORB Keypoint Detection
   ↓
ORB Descriptor Extraction
   ↓
        Matching
   ↑
ORB Descriptor Extraction
   ↑
ORB Keypoint Detection
   ↑
Image 2
   ↓
Candidate Matches
   ↓
Match Filtering
   ↓
RANSAC Verification