import pdfplumber
import csv
from run import image_dict

pdf_path = "/Users/yourname/Desktop/sample_github_sop.pdf"
pdf = pdfplumber.open(pdf_path)

tables = []
page_list = pdf.pages

for page_num, page in enumerate(page_list, start=1):
    page_tables = page.extract_tables()
    for table in page_tables:
        tables.append(table)
        table.append(["Page: ", page_num])

# Collect all insertions
for table in tables:
    insertions = []
    for i, row in enumerate(table):
        if row and row[0] == "Page: ":
            n = int(row[1])
            for image_path in image_dict[n]:
                insertions.append((i, ["Image: ", image_path]))

    # Insert all collected images
    offset = 0
    for index, image_row in insertions:
        table.insert(index + offset, image_row)
        offset += 1

# Save the tables to a CSV file
csv_output_path = "/Users/yourname/Desktop/sample_table_to_csv.csv"
with open(csv_output_path, mode='w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    for table in tables:
        csv_writer.writerows(table)
        csv_writer.writerow([])