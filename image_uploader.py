import argparse
import requests
import io
import os
from os import listdir
from os.path import isfile, join

import datetime
import json
import subprocess
import glob

import firebase_admin
from firebase_admin import credentials, initialize_app, storage
import json
import random
from oauth2client.service_account import ServiceAccountCredentials

from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from helpers.Target import Target
from helpers.Target import getTarget

from image_helper import *

import auth
from auth import getAuthIdTokenForNewUser

import settings
from settings import *

def uploadIssue(enum):
  target = getTarget(enum)
  # Init firebase with your credentials
  cred = credentials.Certificate(getKey(target))
  bucket = getStorageBucket(target)
  initialize_app(cred, {'storageBucket': bucket})

  dir_path = os.path.dirname(os.path.realpath(__file__))
  # Run through the files

  imagePath = ''
  pdfPath = ''
  issue = ''
  files = glob.glob(str(dir_path) + "/issues/*") 
  mydate = datetime.datetime.now()
  month = mydate.strftime("%B")
  year = str(datetime.date.today().year)

  for x in files:
    name = os.path.basename(x)

    bucket = storage.bucket()
    blob = bucket.blob(year + '/' + month + '/' + name)
    blob.upload_from_filename(x)
    blob.make_public()

    if '.jpg' in name:
      imagePath = blob.public_url
    if '.png' in name:
      imagePath = blob.public_url

    if '.pdf' in name:
      pdfPath = blob.public_url
      issue = name.replace('.pdf', '')

  pdfJson = getPdfCellJson(target, imagePath, pdfPath, issue)

  file_name = "issues/issue_uploaded.json"
  
  with open(file_name, 'w') as json_file:
    json.dump(pdfJson, json_file, indent=4, sort_keys=True)
  # Specify the path to your JSON file

  # Get the current directory (app directory)
  # app_directory = os.getcwd()

  # # Construct the file path
  # file_path = os.path.join(app_directory, file_name) 
  
  # if os.path.exists(file_path):
  #   print(f"The file '{file_name}' does exist in the app directory.")

  # # Open the file in Sublime Text 2
  # sublime_command = ['subl', file_path]
  # subprocess.Popen(sublime_command)

  # # Read the contents of the JSON file
  # with open(file_path) as json_file:
  #     data = json.load(json_file)




def uploadImages(enum):
  target = getTarget(enum)
  # Init firebase with your credentials
  cred = credentials.Certificate(getKey(target))
  bucket = getStorageBucket(target)
  initialize_app(cred, {'storageBucket': bucket})

  dir_path = os.path.dirname(os.path.realpath(__file__))
  # Run through the files

  imagePath = ''
  pdfPath = ''
  issue = ''
  files = glob.glob(str(dir_path) + "/issues/*") 
  mydate = datetime.datetime.now()
  month = mydate.strftime("%B")
  year = str(datetime.date.today().year)

  for x in files:
    name = os.path.basename(x)

    bucket = storage.bucket()
    blob = bucket.blob(year + '/' + month + '/' + name)
    blob.upload_from_filename(x)
    blob.make_public()
    imagePath = blob.public_url
    

  pdfJson = getPdfCellJson(target, imagePath, pdfPath, issue)

  with open("issues/issue_uploaded.json", 'w') as json_file:
    json.dump(pdfJson, json_file, indent=4, sort_keys=True)

def test():
  x = '{"hello":"test"}'
  z = json.loads(x)
  for x in ["1", "2", "3", "4"]:
    z.update({"number":x})

  print(json)

def initApp(enum):
  target = getTarget(enum)
  cred = credentials.Certificate(getKey(target))
  initialize_app(cred, {'storageBucket': getStorageBucket(target)})

def uploadFile(name, filePath):

  mydate = datetime.datetime.now()
  month = mydate.strftime("%B")
  year = str(datetime.date.today().year)

  bucket = storage.bucket()
  blob = bucket.blob(year + '/' + month + '/' + name)
  blob.upload_from_filename(filePath)
  blob.make_public()
  return blob.public_url

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--action')
  parser.add_argument('--target', default='SP', const='SP', nargs='?', 
    choices=['BPI', 'BS', 'BCR', 'BFN', 'BAIT', 'FDM', 'IPN', 'PSR', 'SP', 'TN', 'IU'], help = 'Target BPI, BS, BCR, BFN, BAIT, FDM, IPN, PSR, SP, TN, IU')
  args = parser.parse_args()

  if args.action and args.action == 'get' and args.target:
    _get(args.target)
  elif args.action and args.action == 'issue' and args.target:
    uploadIssue(args.target)
  elif args.action and args.action == 'upload' and args.target:
    uploadImages(args.target)
  elif args.action and args.action == 'test':
    test()
  else:
    print('''Invalid command. Please use one of the following commands:
python3 image_uploader.py --action=issue --target BCR
python3 image_uploader.py --action=upload --target BCR
python3 image_uploader.py --action=test
''')

if __name__ == '__main__':
  main()
