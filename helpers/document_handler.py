import argparse
import os
from os import listdir
from os.path import isfile, join

import textract
import json
import pathlib
import glob

from helpers.image.uploader import *
from helpers.document_text_extract import get_json
from helpers.utils import open_in_sublime


def get_files_in_directory(directory_path):
    all_files = [f for f in os.listdir(directory_path) if isfile(join(directory_path, f))]
    doc_files = [f for f in all_files if f.endswith('.doc') or f.endswith('.docx')]  # Include both .doc and .docx files
    image_files = [f for f in all_files if f.endswith('.jpg')]

    files_to_process = []

    for doc_file in doc_files:
        doc_path = join(directory_path, doc_file)
        files_to_process.append((doc_path, image_files))  # Pass all image files in the directory

    return files_to_process

def get_subfolders_for_directory(directory_path):
    subfolders = [f.path for f in os.scandir(directory_path) if f.is_dir()]
    files_to_process = get_files_in_directory(directory_path)

    for subfolder in subfolders:
        if '.git' not in subfolder and '__pycache__' not in subfolder:
            files_to_process.extend(get_subfolders_for_directory(subfolder))

    return files_to_process

def get_menu_name_and_style(path):
    menu_name = ""
    menu_style = ""
    array_by_forward_slash = path.split('/', -1)
    document_name = array_by_forward_slash[-1]

    for item in array_by_forward_slash:
        if "Menu" in item:
            menu_name = item.strip()

    count = len(array_by_forward_slash) - 2
    last_item = array_by_forward_slash[count]

    if "1." in last_item or "Menu" in last_item:
        menu_style = "1"

    return menu_name, menu_style

def extract_text_and_image(path):
    extracted_text = textract.process(path)
    text = extracted_text.decode()

    other_documents_path = pathlib.Path(path).parent
    other_documents = [f for f in os.listdir(other_documents_path) if isfile(join(other_documents_path, f))]

    image_url = ''
    for other_doc_path in other_documents:
        if '.jpg' in other_doc_path:
            full_path = str(other_documents_path) + '/' + str(other_doc_path)
            name = os.path.basename(other_doc_path)
            #image_url = upload_file(name, full_path)

    return text, image_url

def get_json_for_doc_directory(enum, dir_path):
    files_to_process = get_subfolders_for_directory(dir_path)
    json_data = {}
    initApp(enum)

    for doc_path, image_files in files_to_process:
        menu_name, menu_style = get_menu_name_and_style(doc_path)
        document_name = os.path.basename(doc_path)

        text = textract.process(doc_path).decode()
        # Process image files (you can update this part to decide how to associate images with documents)
        image_urls = []
        for image_file in image_files:
            print("Uploading Image...")
            image_path = join(os.path.dirname(doc_path), image_file)
            image_url = upload_file(os.path.basename(image_path), image_path)
            image_urls.append(image_url)

        # Example: use the first image URL or an empty string if there are no images
        image_url = image_urls[0] if image_urls else ''

        if menu_name not in json_data.keys():
            json_data[menu_name] = get_json(document_name, text, image_url, menu_style)
        else:
            current_data = json_data[menu_name]
            new_data = [current_data, get_json(document_name, text, image_url, menu_style)]
            json_data[menu_name] = new_data

    return json_data
    

def main():
  process_document()

if __name__ == '__main__':
  main()
