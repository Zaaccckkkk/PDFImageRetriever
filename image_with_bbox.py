import pdfplumber
import os
from PIL import Image


class BboxFinder:
    """
    Find a new bounding box(bbox) around a pdfplumber-detected image.

    1. Locate the cell in a table where the image is situated.
    2. The bounding box is determined based on the pixel color of the cell.

    This method is often used when images within tables cannot be completely extracted by pymupdf.
    """

    def __init__(self, image, reference_color):
        self.image = image.convert("RGB")
        self.pixels = self.image.load()
        self.reference_color = reference_color

    def is_ref_color(self, pixel, threshold=2):
        """Check whether certain pixel is the required 'reference color'."""
        r, g, b = pixel[:3]
        rr, rg, rb = self.reference_color
        return abs(r - rr) < threshold and abs(g - rg) < threshold and abs(b - rb) < threshold

    def is_x_ref(self, x, y0, y1, threshold=2):
        """Check a whole horizontal line."""
        color_count = 0
        for y in range(int(y0), int(y1)):
            if self.is_ref_color(self.pixels[x, y], threshold=threshold):
                color_count += 1
        return color_count / (y1-y0) > 0.6  # Adjust the percentage yourself.

    def is_y_ref(self, y, x0, x1, threshold=2):
        """Check a whole vertical line."""
        color_count = 0
        for x in range(int(x0), int(x1)):
            if self.is_ref_color(self.pixels[x, y], threshold=threshold):
                color_count += 1
        return color_count / (x1-x0) > 0.6  # Adjust the percentage yourself.

    def find_bbox(self, initial_bbox):
        """Find the new bbox based on the original position of the image, i.e. initial bbox."""
        width, height = self.image.size

        # Get the original position of the image
        initial_left, initial_top, initial_right, initial_bottom = initial_bbox
        x_list = []
        y_list = []

        for x in range(width):
            if self.is_x_ref(x, initial_top, initial_bottom, threshold=2):
                x_list.append(x)

        for y in range(height):
            if self.is_y_ref(y, initial_left, initial_right, threshold=2):
                y_list.append(y)

        # Find the new bbox which is closest to the initial bbox
        if x_list and y_list:
            x0 = max([x for x in x_list if x < initial_left], default=initial_left)
            x1 = min([x for x in x_list if x > initial_right], default=initial_right)
            y0 = max([y for y in y_list if y < initial_top], default=initial_top)
            y1 = min([y for y in y_list if y > initial_bottom], default=initial_bottom)
            return (x0, y0, x1, y1)
        else:
            return None


class PDFImageExtractor:
    """
    Look through the whole PDF and extract all table images with BboxFinder.
    All images are originally detected by pdfplumber.
    """

    def __init__(self, pdf_path, output_folder, reference_color=None):
        self.pdf_path = pdf_path
        self.output_folder = output_folder
        self.pdf = pdfplumber.open(pdf_path)
        self.reference_color = reference_color

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    def extract_images(self):
        image_dict = {}
        previous_bbox = None  # Store the previous bbox
        for page_num, page in enumerate(self.pdf.pages):
            page_key = page_num + 1
            if page_key not in image_dict:
                image_dict[page_key] = []
            page_image_info = page.images
            for img_index, img_info in enumerate(page_image_info):
                img_bbox = (0, 0, page.width, page.height)
                img = page.within_bbox(img_bbox).to_image()
                img_path = os.path.join(self.output_folder, f"page_{page_num+1}_image_{img_index + 1}.png")
                img.save(img_path, format="PNG")

                # Extract the image based on the new bbox
                pil_img = Image.open(img_path)
                initial_bbox = (img_info["x0"], img_info["top"], img_info["x1"], img_info["bottom"])
                bbox_finder = BboxFinder(pil_img, self.reference_color)
                color_bbox = bbox_finder.find_bbox(initial_bbox)
                if color_bbox and color_bbox != previous_bbox:
                    pil_img = pil_img.crop(color_bbox)
                    pil_img.save(img_path, format="PNG")
                    previous_bbox = color_bbox  # Update previous_bbox
                    image_dict[page_key].append(img_path)
                else:
                    os.remove(img_path)  # Delete useless image

        return image_dict
