#!/usr/bin/python3
import os
import textract
import json
import re
from datetime import date

def get_json(documentName, document, imageUrl, style):

  info = {}

  #company name
  company = documentName.replace('.docx',' ')
  company = company.replace('.doc',' ')
  pattern = r'[0-9]'
  # Match all digits in the string and replace them with an empty string
  companyName = re.sub(pattern, '', company)
  if companyName:
      info['CompanyName'] = companyName.strip()

      # #date
  current_date = date.today().strftime('%d/%m/%Y')
  info['Date'] = current_date.strip()

      
  title_pattern = r'^\S(.+)$'
  title = re.findall(title_pattern, document, re.MULTILINE)
  if title:
      info['Title'] = title[0].strip()
  
  description_pattern = r'^(.+)\n'
  description = re.findall(description_pattern, document, re.MULTILINE)
  if description:
      info['Description'] = description[0].strip()
  
  phone_pattern = r'T\s+([\d\s]+)'
  phone = re.findall(phone_pattern, document)
  if phone:
      info['PhoneNumber'] = phone[0].strip()
  
  email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
  email = re.findall(email_pattern, document)
  if email:
      info['Email'] = email[0]
  
  website_pattern = r'(?:https?:\/\/)?(?:[\w-]+\.)+[\w-]+(?:\.[\w-]+)+'
  website = re.findall(website_pattern, document)
  if website:
      info['WebsiteURL'] = updated_url = add_http_www(website[0])

  # Replace \n\n with a placeholder
  temp_placeholder = "TEMP_PLACEHOLDER"
  text = document.replace('\n\n', temp_placeholder)

  # Replace remaining \n with a space
  text = text.replace('\n', ' ')

  # Replace the placeholder with \n\n
  text = text.replace(temp_placeholder, '\n\n')

  removed_title_text = text.split("\n\n", 1)[1]
  
  info['DetailDescription'] = removed_title_text.strip()

  info['Image'] = imageUrl.strip()

  info['CellType'] = "RegularCell"
  info['SortOrder'] = ""

  if style == '1':
    info['CellType'] = "HeaderCell"
    info['SortOrder'] = "1"

  return info

def add_http_www(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    if "://" in url and "www." not in url:
        parts = url.split("://", 1)
        url = parts[0] + "://www." + parts[1]
    return url

def extract_phone_number(text):
    # Example: extract phone number using regular expressions
    match = re.search(r'\b\d{5}\s*\d{6}\b', text)
    return match.group(0) if match else ""

def extract_website_url(text):
    # Example: extract website URL using regular expressions
    match = re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return match.group(0) if match else ""