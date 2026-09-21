# Overlapping Crop Generation

## 1. Overview

Large satellite images can contain a large number of features and may have significant spatial variations.

To make feature matching more manageable and to increase the possibility of finding corresponding local regions, the images are divided into smaller overlapping crops.

---

## 2. Objective

The main objectives of overlapping crop generation are:

- Divide large satellite images into smaller regions
- Preserve local spatial information
- Increase the possibility of finding corresponding areas
- Reduce the computational cost of processing very large images
- Provide suitable inputs for feature detection and matching

---

## 3. Why Overlapping Crops?

Using only the complete satellite image for feature matching may make correspondence detection difficult when:

- The images have different scales
- Only a small region is common between two images
- Large parts of the images contain unrelated areas
- The images come from different sensors

Overlapping crops allow the system to compare smaller local regions instead of relying only on the entire image.

---

## 4. Crop Generation Process

The crop generation pipeline follows:

```text
Input Satellite Image
        ↓
Determine Image Dimensions
        ↓
Define Crop Size
        ↓
Define Overlap
        ↓
Generate Sliding Windows
        ↓
Save Individual Crops
        ↓
Create Crop Metadata
