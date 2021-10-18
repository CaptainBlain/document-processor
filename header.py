#!/usr/bin/python3
import os
import textract
import json
import re
from datetime import date

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

def getJSON(documentName, text, style):
	
	#company name
	company = documentName.replace('.docx',' ')
	company = company.replace('.doc',' ')

	pattern = r'[0-9]'

	# Match all digits in the string and replace them with an empty string
	companyName = re.sub(pattern, '', company)

	#
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

	#date
	current_date = date.today().strftime('%d/%m/%Y')
 
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
		      "CompanyName" : companyName,
		      "Date" : current_date,
		      "Description" : description,
		      "DetailDescription" : detailDescription,
		      "Image" : "",
		      "PhoneNumber" : phoneNumber,
		      "SortOrder" : "1",
		      "Title" : firstLine,
		      "WebsiteURL" : websiteURLString
		      }
		return json

	json = {
	  "CellType" : "RegularCell",
	  "CompanyName" : companyName,
	  "Date" : current_date,
	  "Description" : description,
	  "DetailDescription" : detailDescription,
	  "ThumbnailImage" : "",
	  "PhoneNumber" : phoneNumber,
	  "SortOrder" : "",
	  "Title" : firstLine,
	  "WebsiteURL" : websiteURLString
		}
	return json

	