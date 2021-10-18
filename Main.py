import os
from os import listdir
from os.path import isfile, join

import textract
import json

from header import getJSON
#from regular import getRegularJSON
#Get the current directory
dir_path = os.path.dirname(os.path.realpath(__file__))

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
	#Get any Docuemnts
	documents = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]
	#print(documents)
	for doc in documents:
		if '.doc' in doc:		
			documentsPaths.append(join(directory_path, doc))
	for subFolder in subfolders:
		#Ignore the folders we don't need
		if '.git' not in subFolder and '__pycache__' not in subFolder:
			getSubFoldersForDirecory(subFolder)


getSubFoldersForDirecory(dir_path)


jsonData = {}
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

	extractedText = textract.process(path)
	text = extractedText.decode()	
	#print(menuName)
	if menuName not in jsonData.keys():	
		#print(menuName)		
		jsonData[menuName] = getJSON(documentName, text, menuStyle)
	else:
		currentData = jsonData[menuName]
		#print(currentData)
		newData = [currentData, getJSON(documentName, text, menuStyle)]
		jsonData[menuName] = newData

	#jsonData.append(getJSON(text))


jsonDict = {
	"output":jsonData
}


#documentName = documentName.replace('.doc', '')
#jsonFile = documentName.replace(' ', '_')
with open("sample.json", 'w') as json_file:
    json.dump(jsonDict, json_file)
