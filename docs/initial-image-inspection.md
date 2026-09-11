# Initial Image Inspection

## ১. Image Information

- File name: `ohrc_01.tif`
- Instrument: OHRC
- Image type: Annotated OHRC image
- Source: To be verified
- Image format: TIFF
- Image shape: `(956, 1023, 3)`
- Image height: `956 pixels`
- Image width: `1023 pixels`
- Number of channels: `3`
- Data type: `uint8`
- Minimum pixel value: `0`
- Maximum pixel value: `255`

## ২. Visual Observation

The image contains a lunar surface captured by the Chandrayaan-2 OHRC instrument.

The image is not a clean raw satellite image. It contains additional annotations and presentation elements, such as:

- ISRO logo
- Chandrayaan-2 label
- Text describing the image
- Red bounding box
- Scale bar
- Altitude information
- Pixel resolution information
- Sun elevation angle
- Date information

The lunar surface contains several visible features, including:

- Impact craters
- Rocks or boulders
- Bright and dark surface regions
- Shadows
- Uneven lunar terrain

The image appears to be a three-channel image. The pixel values range from 0 to 255, which is consistent with an 8-bit image.

## ৩. Image Quality

- Image clarity: The lunar surface features are visible.
- Brightness: Different bright and dark regions are present.
- Contrast: The image has visible contrast between the surface and shadows.
- Noise: No major noise problem was observed visually.
- Annotation: The image contains text, labels, and a red box.
- Raw image status: This appears to be an annotated image rather than a raw satellite image.

## ৪. Initial Problems

The following problems may affect image matching:

1. The image contains text and graphical annotations.
2. The red bounding box may create unwanted feature points.
3. The scale bar may create false matching features.
4. The black background and labels may interfere with feature extraction.
5. The image may not contain the original scientific metadata.
6. The image may not be suitable for direct quantitative evaluation.
7. The actual raw OHRC image still needs to be collected and inspected.

## ৫. Important Image Details

The displayed image mentions the following information:

- Altitude: Approximately 100 km
- Pixel resolution: 30 cm
- Sun elevation angle: 7.8 degrees
- Date: 05 September 2019
- Scale bar: 25 m

These details are visible in the image, but they should be verified from the original data source or metadata before being used in the final project.

## ৬. Conclusion

The image was successfully loaded using OpenCV.

The image shape is `(956, 1023, 3)`, its data type is `uint8`, and its pixel values range from 0 to 255.

The image contains visible lunar surface features, but it also contains annotations, labels, and graphical elements. Therefore, this image should be treated as a sample or reference image.

For the actual image correspondence project, clean raw OHRC, TMC, and IIRS images should be collected. These raw images will be used for preprocessing, feature extraction, matching, and evaluation.

