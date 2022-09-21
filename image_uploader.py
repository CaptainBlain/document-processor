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
from realtime_database_worker import helpers
from realtime_database_worker.helpers.Target import Target
from realtime_database_worker.helpers.Target import getTarget

from image_helper import *

import realtime_database_worker.auth
from realtime_database_worker.auth import getAuthIdTokenForNewUser

import realtime_database_worker.settings
from realtime_database_worker.settings import *

def uploadIssue(enum):
  target = getTarget(enum)
  # Init firebase with your credentials
  cred = credentials.Certificate(getKey(target))
  initialize_app(cred, {'storageBucket': getStorageBucket(target)})

  dir_path = os.path.dirname(os.path.realpath(__file__))
  # Run through the files

  imagePath = ''
  pdfPath = ''
  issue = ''
  files = glob.glob(str(dir_path) + "/images/*") 
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

  with open("images/issue_uploaded.json", 'w') as json_file:
    json.dump(pdfJson, json_file, indent=4, sort_keys=True)

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
    choices=['BPI', 'BS', 'BCR', 'BFN', 'BAIT', 'FDM', 'IPN', 'PSR', 'SP', 'TN'], help = 'Target BPI, BS, BCR, BFN, BAIT, FDM, IPN, PSR, SP, TN')
  args = parser.parse_args()

  if args.action and args.action == 'get' and args.target:
    _get(args.target)
  elif args.action and args.action == 'issue' and args.target:
    _uploadIssue(args.target)
  elif args.action and args.action == 'upload' and args.target:
    _uploadImagesManual(args.target)
  else:
    print('''Invalid command. Please use one of the following commands:
python3 image_uploader.py --action=issue --target BCR
python3 image_uploader.py --action=upload --target BCR
''')

if __name__ == '__main__':
  main()
