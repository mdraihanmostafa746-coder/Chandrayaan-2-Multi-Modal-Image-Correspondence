




## Dataset Validation and Visual Analysis

The dataset contains five clean lunar images from the OHRC and TMC-2 instruments.

Dataset validation confirmed that:

- All five images are present.
- All five images are readable.
- The images have different spatial dimensions.
- Pixel data is stored in uint8 format.
- Grayscale conversion and Canny edge detection were applied.
- Pixel intensity histograms were generated for visual analysis.

The visual analysis helps identify lunar surface structures such as craters, boulders, ridges, and edges before feature matching.

## Preprocessing

All five images were processed using a common preprocessing pipeline.

The pipeline includes:

1. Image resizing to 512 × 512 pixels.
2. Grayscale conversion.
3. Min-max pixel normalization.
4. Saving the processed images in PNG format.

The processed images will be used for cropping, feature extraction, and image matching experiments.

