# PDFImageRetriever

PDFImageRetriever is a Python tool designed to extract images from PDF documents and detect their bounding boxes and dominant colors, mainly suitable for PDFs containing tables and with post-annotations in images. This tool utilizes `pdfplumber` for PDF parsing and `PIL` (Pillow) for image processing.

## Features

- Extract images from PDF documents.
- Locate bounding boxes around images within tables.
- Detect the most common colors in the extracted images.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Zaaccckkkk/PDFImageRetriever.git
   cd PDFImageRetriever

2. Download the [sample_border_line.png](sample_border_line.png) and [sample_github_sop.pdf](sample_github_sop.pdf) to give a test.

3. Run the sample files:

   ```bash
   python run.py

## File Description

1. [detect_color.py](detect_color.py):

(a) Use class ColorDetector to analyze the RGB image of the border line of a table in pdf file, traverse each pixel in the image, get the color of the pixel and record the number of times each color appears.

(b) Return the most common color.

2. [image_with_bbox.py](image_with_bbox.py):

(a) Use class BboxFinder to get the nearest border of the image we want to capture.

(b) class PDFImageExtractor helps to extract the image from the whole page using the coordinates of the nearest border.

(c) Render a high resolution image by adjust DPI.

