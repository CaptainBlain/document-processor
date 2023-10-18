import argparse
import os
from os import listdir
from os.path import isfile, join

import textract
import json
import pathlib
import glob
import time

from helpers.image.uploader import *
from helpers.image.screenshot_pdf import extract_first_page_image

from helpers.document_handler import get_json_for_doc_directory
from helpers.utils import open_in_sublime, start_loading_animation


#Get the current directory
doc_path = str(os.path.dirname(os.path.realpath(__file__))) + '/export/doc'
issues_path = str(os.path.dirname(os.path.realpath(__file__))) + '/export/issues'

def take_pdf_screenshot():

	dir_path = os.path.dirname(os.path.realpath(__file__))
	files = glob.glob(str(dir_path) + "/export/issues/*") 
	for x in files:
		pdf_name = os.path.basename(x)
		old_extension = os.path.splitext(pdf_name)[1]
		new_extension = ".png"
		new_file_name = pdf_name.replace(old_extension, new_extension)
		pdf_path = os.path.abspath(x)
		extract_first_page_image(pdf_path, issues_path + '/' + new_file_name)


def processFile(enum):
	print("Processing file...")
	# Start the loading animation
	loading_thread, stop_loading = start_loading_animation()
	jsonData = get_json_for_doc_directory(enum, doc_path)
	file_name = "export/doc/processed_data.json"
	with open(file_name, 'w') as json_file:
	    	json.dump(jsonData, json_file, indent=4, sort_keys=True)
	#Stop the loading animation
	stop_loading()
	loading_thread.join()
	open_in_sublime(file_name)
	


def processIssue(enum):
	print("Taking Screenshot")
	# Start the loading animation
	loading_thread, stop_loading = start_loading_animation()
	take_pdf_screenshot()
	print("Uploading issue")
	pdfJson = upload_issue(enum, issues_path)
	file_name = "export/issues/issue_uploaded.json"
	with open(file_name, 'w') as json_file:
	    	json.dump(pdfJson, json_file, indent=4, sort_keys=True)
	open_in_sublime(file_name)
	# Stop the loading animation
	stop_loading()
	loading_thread.join()
	
def processBoth(enum):
	print("process Issue")
	processIssue(enum)
	print("process File")
	processFile(enum)
	print("Published both")

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--action')
  parser.add_argument('--target', default='SP', const='SP', nargs='?', 
    choices=['BPI', 'BS', 'BCR', 'BFN', 'BAIT', 'FDM', 'IPN', 'PSR', 'SP', 'TN', 'IU'], help = 'Target BPI, BS, BCR, BFN, BAIT, FDM, IPN, PSR, SP, TN, IU')
  args = parser.parse_args()

  if args.action and args.action == 'file' and args.target:
    processFile(args.target)
  elif args.action and args.action == 'issue' and args.target:
    processIssue(args.target)
  elif args.action and args.action == 'both' and args.target:
   	processBoth(args.target)
  else:
    print('''Invalid command. Please use one of the following commands:
	python3 process_docs.py --action=file --target BAIT
	python3 process_docs.py --action=issue --target 
	python3 process_docs.py --action=both --target 
''')

if __name__ == '__main__':
  main()
