import argparse
import requests
import io
import os
import subprocess

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import random
from oauth2client.service_account import ServiceAccountCredentials

from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from helpers.Target import Target
from helpers.Target import getTarget

from auth import getAuthIdTokenForNewUser

import settings
from settings import *

def getUrl(target, authToken):
   return getRemoteConfigUrl(target) + '.json?print=pretty&auth=' + authToken

def _getAccessToken(target):
  key = getKey(target)
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      key, settings.SCOPES)
  access_token_info = credentials.get_access_token()
  return access_token_info.access_token


def _get(enum):
  target = getTarget(enum)

  accessToken = _getAccessToken(target);
  url = getUrl(target, accessToken)

  resp = requests.get(url)
  
  if resp.status_code == 200:
    filename = getContentFileName(target)
    
    with io.open(filename, 'wb') as f:
      f.write(resp.text.encode('utf-8'))
    print('Retrieved data has been written to ' + getContentFileName(target))
  else:
    print('Unable to get realtime database')
    print(resp.text)


def _publish(enum):
  target = getTarget(enum)
  
  idToken = getAuthIdTokenForNewUser(target)

  with open(getContentFileName(target), 'r', encoding='utf-8') as f:
    content = f.read()
  
  headers = {
    'Content-Type': 'application/json; UTF-8'
  }

  url = getUrl(target, str(idToken))
  
  resp = requests.put(url, data=content.encode('utf-8'), headers=headers)
  if resp.status_code == 200:
    print('Database update has been published.')
  else:
    print('Unable to publish database update.')
    print(resp.text)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--action')
  parser.add_argument('--target', default='SP', const='SP', nargs='?', 
    choices=['BPI', 'BS', 'BCR', 'BFN', 'BAIT', 'FDM', 'IPN', 'PSR', 'SP', 'TN', 'IU'], help = 'Target BPI, BS, BCR, BFN, BAIT, FDM, IPN, PSR, SP, TN, IU')
  args = parser.parse_args()

  if args.action and args.action == 'get' and args.target:
    _get(args.target)
  elif args.action and args.action == 'publish' and args.target:
    _publish(args.target)
  else:
    print('''Invalid command. Please use one of the following commands:
python3 process_database.py --action=get --target BAIT
python3 process_database.py --action=publish --target BAIT
''')

if __name__ == '__main__':
  main()
