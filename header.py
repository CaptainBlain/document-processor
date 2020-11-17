import os
import textract
import json


def stripAndFind(fullString, toFind):
	returnString = ""
	if toFind in fullString:
		attemptToSplit = fullString.split("\n")
		if len(attemptToSplit) > 1 :
			for subItem in attemptToSplit:
				if toFind in subItem:
					returnString = subItem
					break
		else:
			returnString = fullString.strip()
	return returnString

def getJSON(text, style):
	
	arrayByDoubleLineBreak = text.split('\n\n', -1)

	firstLine = ""
	description = ""
	detailDescription = ""

	if len(arrayByDoubleLineBreak) > 1 :
		firstLine = arrayByDoubleLineBreak[0]
		#Delete the title out of the text
		del arrayByDoubleLineBreak[0]
		#Join the text back together
		detailDescription = ''.join(arrayByDoubleLineBreak)
	else:
		arrayBySingleLineBreak = text.split('\n')
		if len(arrayBySingleLineBreak) > 1 :		
			firstLine = arrayBySingleLineBreak[0]
			#Delete the title out of the text
			del arrayBySingleLineBreak[0]
			#Join the text back together
			detailDescription = ''.join(arrayBySingleLineBreak)

	#Title tidy
	firstLine = firstLine.replace('\n',' ')

	#We should have the detailDescription
	splitByFullStop = detailDescription.split('.')
	#We need to grab the first sentence out fot the desc
	if len(splitByFullStop) > 1 :
		description = splitByFullStop[0]

	#description tidy
	description = description.replace('\n',' ')

	phoneNumber = ""
	websiteURL = ""
	for item in text.split("\n\n"):
		websiteURL = stripAndFind(item, "www.")
		phoneNumber = (stripAndFind(item, "T ")).replace('T ', '')
		
	#Phone number tidy	
	phoneNumber = phoneNumber.replace('+44', '0')	
	
	websiteURLString = websiteURL
	if "http" not in websiteURL:
		websiteURLString = "http://" + websiteURL

	if style == '1':
		json = {
		      "CellType" : "HeaderCell",
		      "CompanyName" : "",
		      "Description" : description,
		      "DetailDescription" : text,
		      "Image" : "",
		      "PhoneNumber" : phoneNumber,
		      "SortOrder" : "1",
		      "Title" : firstLine,
		      "WebsiteURL" : websiteURLString
		      }
		return json

	json = {
	  "CellType" : "RegularCell",
	  "CompanyName" : "",
	  "Description" : description,
	  "DetailDescription" : text,
	  "ThumbnailImage" : "",
	  "PhoneNumber" : phoneNumber,
	  "SortOrder" : "",
	  "Title" : firstLine,
	  "WebsiteURL" : websiteURLString
		}
	return json

	