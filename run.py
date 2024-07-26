from detect_color import ColorDetector
from image_with_bbox import PDFImageExtractor


# Change the paths below to match your file locations
image_path = "/Users/yourname/Desktop/sample_border_line.png"
pdf_path = "/Users/yourname/Desktop/sample_github_sop.pdf"
output_folder = "/Users/yourname/Desktop/get_page_images"
output_folder2 = "/Users/yourname/Desktop/get_useful_images"

ColorDetector(image_path).print_top_colors()
color = ColorDetector(image_path).get_top_color()
image_extractor = PDFImageExtractor(pdf_path, output_folder, output_folder2, reference_color=[color])
image_dict = image_extractor.extract_images()
