import os
from os import listdir
from os.path import isfile, join
import sys
import fitz # PyMuPDF package for PDF processing 'pip3 install PyMuPDF'


def extract_first_page_image(pdf_path, image_path):

	if not os.path.isfile(pdf_path):
		print("Error: File {pdf_path} not found.")
		return

	with fitz.open(pdf_path) as doc:
		page = doc[0]
		pix = page.get_pixmap()
		pix.save(image_path)
		

# def extract_first_page_image(pdf_path, image_path):
# 	print("extract_first_page_image: " + pdf_path)
# 	print("extract_first_page_image: " + image_path)
#     # Check if the input PDF file exists
#     if not os.path.isfile(pdf_path):
#         print(f"Error: File {pdf_path} not found.")
#         return

#     # Open the PDF file
#     with fitz.open(pdf_path) as doc:
#         # Get the first page of the PDF
#         page = doc[0]
#         # Convert the page to an image
#         pix = page.get_pixmap()
#         # Save the image as a PNG file
#         pix.save(image_path)

#     print(f"Image saved to {image_path}")

# if __name__ == "__main__":
#     # Get the path to the input PDF file
#     pdf_path = sys.argv[1]
#     # Create the subfolder for the PNG image
#     image_folder = os.path.join(os.path.dirname(pdf_path), "images")
#     os.makedirs(image_folder, exist_ok=True)
#     # Create the filename for the PNG image
#     image_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".png"
#     image_path = os.path.join(image_folder, image_filename)
#     # Extract the first page of the PDF as an image and save it as a PNG file
#     extract_first_page_image(pdf_path, image_path)
