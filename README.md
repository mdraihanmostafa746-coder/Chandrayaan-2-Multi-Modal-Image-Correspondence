# Chandrayaan-2 Multi-Modal Image Correspondence

## Problem Statement

**Multi-modal, Sun-angle and Scale-invariant Image Correspondence using Chandrayaan-2 Optical Images (OHRC, TMC and IIRS).**

The objective of this project is to identify corresponding regions between Chandrayaan-2 optical images acquired under different imaging conditions.

The system focuses on feature-based image correspondence using image preprocessing, feature detection, descriptor matching and geometric verification.

---

## Proposed Solution

The proposed system follows a computer vision pipeline for identifying reliable image correspondences.

The pipeline performs the following major operations:

1. Dataset validation and image inspection
2. Image preprocessing
3. Overlapping crop generation
4. ORB feature detection
5. Feature descriptor matching
6. Match filtering using Lowe's Ratio Test
7. RANSAC-based geometric verification
8. Matching score evaluation
9. Cross-sensor correspondence analysis
10. Interactive visualization using Streamlit

The system also includes baseline and robustness experiments using SIFT, CLAHE, Gaussian Blur, scale variations and synthetic illumination variations.

---

## System Pipeline

```text
Chandrayaan-2 Optical Images
            │
            ▼
     Dataset Validation
            │
            ▼
      Image Inspection
            │
            ▼
     Image Preprocessing
            │
            ▼
   Overlapping Crop Generation
            │
            ▼
      ORB Feature Detection
            │
            ▼
     Descriptor Matching
            │
            ▼
      Lowe's Ratio Test
            │
            ▼
    RANSAC Geometric Verification
            │
            ▼
      Matching Evaluation
            │
            ▼
     Correspondence Visualization
            │
            ▼
       Streamlit Web Interface