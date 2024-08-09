# PDFImageRetriever

PDFImageRetriever is a Python tool designed to extract images from tables in PDF documents through detecting their bounding boxes and dominant colors of the boxes, especially suitable for PDFs containing tables with post-annotated images. This tool utilizes `pdfplumber` for PDF parsing and `PIL` (Pillow) , `fitz` (pymupdf) for image processing.

## Features

- Extract images from PDF documents.
- Locate bounding boxes around images within tables.
- Detect the most common colors in the extracted images.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Zaaccckkkk/PDFImageRetriever.git
   cd PDFImageRetriever

2. Install requirements

   We highly recommend creating a new virtual environment(venv) in a location of your choice and installing all requirements into the venv.
   Create your venv:
   ```bash
   python3.11 -m venv your_venv
   ```
   
   Activate your venv:
   ```bash
   source your_venv/bin/activate
   ```

   Install the requirements to your venv:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the [sample_border_line.png](sample_border_line.png) and [sample_github_sop.pdf](sample_github_sop.pdf) to give a test.

- sample_border_line.png contains a simple border line used for testing the bounding box detection functionality. The black line in the middle of the image is intended to simulate a border that the `BboxFinder` class can detect and use to determine the bounding box.

- sample_github_sop.pdf contains embedded images that can be extracted and analyzed using the provided tools.

4. Run the sample files:

   ```bash
   python run.py

5. Convert the table to csv file:

   ```bash
   python sample_table_to_csv.py

## File Description

1. [detect_color.py](detect_color.py):

- Use `ColorDetector` class to analyze the RGB image of the border line of a table in pdf file, traverse each pixel in the image, get the color of the pixel and record the number of times each color appears.

- Return the most common color.

2. [image_with_bbox.py](image_with_bbox.py):

- Use `BboxFinder` class to get the nearest border of the image we want to capture.

- `PDFImageExtractor` class helps to extract the image from the whole page using the coordinates of the nearest border.

- Render a high resolution image by adjusting DPI.

3. [run.py](run.py):

- Apply `detect_color` and `image_with_bbox` on the sample `.png` and `.pdf`

- Put the result images into folders

## An SOP PDF example
<img width=55% alt="example_page" src="https://github.com/user-attachments/assets/398bf485-d55a-4bb7-96b9-73d8d72001f6"> <img width=44% alt="example_border_line" src="https://github.com/user-attachments/assets/ecc7b5bb-45ff-4750-b244-fc7d354d64a0">

I created a simple SOP PDF file (example_github_sop.pdf) that contains annotated images within the tables.

The left image above shows one page of the example_github_sop.pdf. I then get the right image above(example_border_line.png) by zooming in.

Then, after running the `run.py`, we output all the images in the folder `get_images_useful`.

<img width=99% src="https://github.com/user-attachments/assets/15126ece-e54a-40aa-9d36-d39c5e26dee4">

Each output image is a cell containing the original image. In this way, we successfully incorporated the annotations within the images in the table.
