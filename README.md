# Chandrayaan-2 Multi-Modal Image Correspondence

## Problem Statement
Multi-modal, sun-angle and scale-invariant image correspondence using Chandrayaan-2 optical images.

## Current Pipeline
1. Dataset validation
2. Image preprocessing
3. Overlapping crop generation
4. Feature detection and matching
5. RANSAC-based geometric verification
6. Matching evaluation
7. Best-match ranking

## Project Structure
- data/raw: Raw satellite images
- data/processed: Preprocessed images and crops
- src: Processing and matching scripts
- results: Evaluation and visualization outputs
- run_pipeline.py: Automated pipeline runner

## How to Run

```bash
python3 run_pipeline.py