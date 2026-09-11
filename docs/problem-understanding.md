
# Problem Understanding


## 1. What is the Problem?

    This problem is about building an AI system that can identify the same location on the Moon 
    from images captured by different Chandrayaan-2 instruments, even when the lighting and 
    image scale are different.


## 2. What is Image Correspondence?

    Image Correspondence means finding the same physical location or matching points in two different images.

        For example, if OHRC and TMC both capture the same lunar crater, 
        the AI system identifies which points in the OHRC image 
        correspond to the same points in the TMC image.


## 3. What does Multi-Modal Mean?

    Multi-Modal means using images or data from different types of sensors or instruments.

In this problem, OHRC, TMC, and IIRS capture different kinds of information about the Moon. 
The AI system must find matching locations across these different image types.


## 4. What is Scale Invariance?

    Scale Invariance means the AI system can identify the same lunar surface location even when one 
    image is zoomed in and the other is zoomed out.


## 5. What is Sun-Angle Invariance?

    Sun-Angle Invariance means the AI system can identify the same lunar surface location even when the Sun 
    illuminates the terrain from different angles, causing changes in shadows and brightness.


## 6. What are OHRC, TMC and IIRS?

    * OHRC: Orbiter High Resolution Camera — captures detailed, high-resolution images of the lunar surface.

    * TMC: Terrain Mapping Camera — captures images used to map the Moon's terrain and elevation.

    * IIRS: Imaging Infrared Spectrometer — captures spectral information to study the Moon's surface composition.


## 7. Why is This Problem Difficult?

    This problem is difficult because the same lunar surface can look different due to changes in sensor type, Sun angle, 
    shadows, brightness, and image scale. The AI must still identify the correct matching locations.


## 8. Expected Input

    Two or more lunar images captured by Chandrayaan-2 instruments (OHRC, TMC, or IIRS), possibly with different 
    Sun angles, scales, and sensor types.


## 9. Expected Output

    The AI system should identify matching points or regions in the input images and provide correspondence results 
    with confidence scores.


## 10. Our Initial Understanding

    We need to build an AI-based image matching system that identifies the same lunar surface locations across 
    OHRC, TMC, and IIRS images, despite differences in sensor type, Sun angle, and image scale.

