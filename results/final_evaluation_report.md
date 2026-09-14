# Final Evaluation and Best Method Selection

## Method Comparison

| Method | Matching Score |
|---|---:|
| ORB | 0.5974 |
| SIFT | 0.1523 |
| ORB + CLAHE | 0.5342 |
| ORB + Gaussian Blur | 0.7377 |

## Best Method

ORB + Gaussian Blur achieved the highest matching score of 0.7377
on the current crop pair.

## Observation

Gaussian Blur improved the matching score compared with the original
ORB baseline. CLAHE increased the number of keypoints but reduced the
matching score. SIFT produced the lowest score on this crop pair.

This result is preliminary and should be re-evaluated after adding
more OHRC, TMC, and IIRS images.
