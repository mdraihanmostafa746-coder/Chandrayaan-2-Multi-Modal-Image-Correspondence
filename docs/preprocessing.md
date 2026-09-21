# Image Preprocessing

## 1. Overview

Image preprocessing is an important step in the satellite image correspondence pipeline. The objective of preprocessing is to prepare the input images for reliable feature detection and matching.

The preprocessing stage was designed to maintain important image structures while reducing unnecessary variations that could affect feature matching.

---

## 2. Input Images

The project uses optical satellite images from the Chandrayaan-2 mission, including data from:

- OHRC (Orbiter High Resolution Camera)
- TMC (Terrain Mapping Camera)
- IIRS (Imaging Infrared Spectrometer)

The available images were inspected before applying preprocessing.

---

## 3. Preprocessing Steps

The preprocessing pipeline includes the following operations:

1. Image loading
2. Image validation
3. Image format and dimension checking
4. Conversion to grayscale where required
5. Intensity normalization where applicable
6. Preparation of images for feature detection and matching

---

## 4. Image Validation

Before preprocessing, each image is checked for:

- Image dimensions
- Number of channels
- Data type
- Pixel value range
- Image readability

For example, one inspected image had:

```text
Shape: (956, 1023, 3)
Data type: uint8
Pixel range: 0 - 255