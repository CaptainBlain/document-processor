import argparse
import os
from os import listdir
from os.path import isfile, join

import textract
import json
import pathlib

from image_uploader import initApp, uploadFile, uploadIssue
from header import getJSON

from helpers.Target import Target
from helpers.Target import getTarget

#Get the current directory
dir_path = str(os.path.dirname(os.path.realpath(__file__))) + '/doc'

#List the files
#for f in listdir(dir_path):
	#if isfile(join(dir_path, f)):
		#doc = join(dir_path, f)
		#if '.doc' in doc:
			#print(doc)


documentsPaths = []
documentName = ""
def getSubFoldersForDirecory(directory_path):
	#Get any subfolders
	subfolders = [f.path for f in os.scandir(directory_path) if f.is_dir() ]   
	#print(subfolders)
	#Get any Docuemnts
	documents = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
	
	for doc in documents:
		if '.doc' in doc:		
			documentsPaths.append(join(directory_path, doc))
	for subFolder in subfolders:
		#Ignore the folders we don't need
		if '.git' not in subFolder and '__pycache__' not in subFolder:
			getSubFoldersForDirecory(subFolder)


def processFile(enum):
	getSubFoldersForDirecory(dir_path)

	jsonData = {}
	initApp(enum)
	for path in documentsPaths:
		#print(path)
		menuName = ""
		menuStyle = ""
		arrayByForwardSlash = path.split('/', -1)
		documentName = arrayByForwardSlash[-1]

		for item in arrayByForwardSlash:
			if "Menu" in item:
				menuName = item.strip()

		count = len(arrayByForwardSlash) - 2
		
		lastItem = arrayByForwardSlash[count]
		#print(lastItem)
		if "1." in lastItem:
			menuStyle = "1"
		if "Menu" in lastItem:
			menuStyle = "1"

		text = ''
		imageUrl = ''
		if '.doc' in path:	
			extractedText = textract.process(path)
			text = extractedText.decode()	
		
		otherDocumentsPath  = pathlib.Path(path).parent
		otherDocuments = [f for f in listdir(otherDocumentsPath) if isfile(join(otherDocumentsPath, f))]
		for otherDocPath in otherDocuments:

			if '.jpg' in otherDocPath:
				fullPath = str(otherDocumentsPath) + '/' + str(otherDocPath)
				name = os.path.basename(otherDocPath)
				imageUrl = uploadFile(name, fullPath)

		if menuName not in jsonData.keys():	
			#print(menuName)		
			jsonData[menuName] = getJSON(documentName, text, imageUrl, menuStyle)
		else:
			currentData = jsonData[menuName]
			#print(currentData)
			newData = [currentData, getJSON(documentName, text, imageUrl, menuStyle)]
			jsonData[menuName] = newData


	#documentName = documentName.replace('.doc', '')
	#jsonFile = documentName.replace(' ', '_')
	with open("doc/processed_data.json", 'w') as json_file:
	    json.dump(jsonData, json_file, indent=4, sort_keys=True)

	print("Published file")    
	#with open("doc/processed_data.json", 'w') as json_file:
    #json.dump(jsonData, json_file, indent=4, sort_keys=True)

def processIssue(enum):
	uploadIssue(enum)
	print("Published issue")

def processBoth(enum):
	processFile(enum)
	uploadIssue(enum)
	print("Published both")

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--action')
  parser.add_argument('--target', default='SP', const='SP', nargs='?', 
    choices=['BPI', 'BS', 'BCR', 'BFN', 'BAIT', 'FDM', 'IPN', 'PSR', 'SP', 'TN'], help = 'Target BPI, BS, BCR, BFN, BAIT, FDM, IPN, PSR, SP, TN')
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
