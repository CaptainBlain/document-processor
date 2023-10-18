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

from auth_dp.target import get_target
from auth_dp.auth import get_auth_id_token_for_new_user
from auth_dp.settings import *

from helpers.image.helper import get_pdf_cell_json, get_storage_bucket, get_key


def get_all_files(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file != '.DS_Store':
                file_list.append(os.path.join(root, file))
    return file_list

def upload_issue(enum, path):
  target = get_target(enum)
  # Init firebase with your credentials
  cred = credentials.Certificate(get_key(target))
  bucket = get_storage_bucket(target)
  initialize_app(cred, {'storageBucket': bucket})

  dir_path = os.path.dirname(os.path.realpath(__file__))
  # Run through the files

  imagePath = ''
  pdfPath = ''
  issue = ''
  files = get_all_files(path)
  mydate = datetime.datetime.now()
  month = mydate.strftime("%B")
  year = str(datetime.date.today().year)

  print(files)
  for x in files:
    name = os.path.basename(x)
    print(name)
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


  return get_pdf_cell_json(target, imagePath, pdfPath, issue)


def uploadImages(enum):
  target = get_target(enum)
  # Init firebase with your credentials
  cred = credentials.Certificate(get_key(target))
  bucket = get_storage_bucket(target)
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
    

  pdfJson = get_pdf_cell_json(target, imagePath, pdfPath, issue)

  with open("issues/issue_uploaded.json", 'w') as json_file:
    json.dump(pdfJson, json_file, indent=4, sort_keys=True)

def test():
  x = '{"hello":"test"}'
  z = json.loads(x)
  for x in ["1", "2", "3", "4"]:
    z.update({"number":x})

  print(json)

def initApp(enum):
  target = get_target(enum)
  cred = credentials.Certificate(get_key(target))
  initialize_app(cred, {'storageBucket': get_storage_bucket(target)})

def upload_file(name, filePath):

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
