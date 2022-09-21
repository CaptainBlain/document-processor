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
from enum import Enum
from firebase.firebase import FirebaseApplication, FirebaseAuthentication

#Run this in terminal before (Live)
#find filepath with: realpath -s service-account.json
#export GOOGLE_APPLICATION_CREDENTIALS="/{file-location}/service-account.json"
#GOOGLE_APPLICATION_CREDENTIALS="/Users/blainellis/Desktop/Solutions Publishing Remote/bait-service-account.json"
#GOOGLE_APPLICATION_CREDENTIALS="//Users/blainellis/Documents/remore-config-access/service-account-sandbox.json"

PROJECT_ID_LIVE = 'businessandindustrytoday'
REMOTE_CONFIG_URL = 'https://businessandindustrytoday.firebaseio.com/'
SCOPES = [
  "https://www.googleapis.com/auth/firebase.database"
]

KEY_LIVE = os.path.join(os.path.dirname(__file__), 'bait-service-account.json')
JSON_FILE = os.path.join(os.path.dirname(__file__), 'config.json')
#Get the service.account.json from Firebase project settings->Service accounts"
  

class Target(Enum):
    LIVE = 'LIVE'
    SANDBOX = 'SANDBOX'
    DEV = 'DEV'

def _get_remote_config_url(accessToken):
  url = REMOTE_CONFIG_URL + '.json?print=pretty&access_token=' + accessToken
  return url     

def _get_content_file_name(target):
  fileName = 'bait-realtime-database.json'
  if target == Target.SANDBOX:
     fileName = 'config.json'
  return fileName  

def _get_access_token(target):
  """Retrieve a valid access token that can be used to authorize requests.
  :return: Access token.
  """
  key = KEY_LIVE
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      key, SCOPES)
  access_token_info = credentials.get_access_token()
  return access_token_info.access_token

def _get2(enum):
  target = Target(enum)
  """Retrieve the current Firebase Remote Config template from server.
  Retrieve the current Firebase Remote Config template from server and store it
  locally.
  """
  #cred = credentials.Certificate(KEY_LIVE) 
  #firebase_admin.initialize_app(cred)
 
  #firebase = FirebaseApplication(REMOTE_CONFIG_URL, None)
  #result = firebase.get('/', None)


  # Use the credentials object to authenticate a Requests session.
  #authed_session = AuthorizedSession(credentials)
  #response = authed_session.get(DATABASE_NAME+ ".json")


  #with open (JSON_FILE) as data_file: data = json.load(data_file)
  #jsondata = json.dumps(JSON_FILE)
    
  #requests.put(url=REMOTE_CONFIG_URL, json= jsondata)


def _get(enum):
  target = Target(enum)

  accessToken = _get_access_token(target);
  url = REMOTE_CONFIG_URL + '.json?print=pretty&auth=' + accessToken

  resp = requests.get(url)
  
  if resp.status_code == 200:
    with io.open(_get_content_file_name(target), 'wb') as f:
      f.write(resp.text.encode('utf-8'))
    print('Retrieved data has been written to ' + _get_content_file_name(target))
  else:
    print('Unable to get realtime database')
    print(resp.text)

def _auth(target):

  headers = {
    'Content-Type': 'application/json; UTF-8'
  }
  body = {
    'token': _get_access_token(target),
    'returnSecureToken': True
  }

  apiKey = 'AIzaSyAqkUaaRHT7Rc96zt-WQu7WVdPp4WtpCJA'
  url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key=' + apiKey
  resp = requests.post(url, data=body, headers=headers)
  print(resp)

def _auth_email():

  url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyAqkUaaRHT7Rc96zt-WQu7WVdPp4WtpCJA"

  ranno = random.randint(100000,999999999)
  payload = json.dumps({
    "email": "blain.ellis+" + str(ranno) + "@example.com",
    "password": "PASSWORD",
    "returnSecureToken": True
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  data = response.json()
  #print(data)
  idToken = data.get('idToken')
  #print(idToken)
  return idToken


def _publish(enum):
  target = Target(enum)
  """Publish local template to Firebase server.
  Args:
    etag: ETag for safe (avoid race conditions) template updates.
        * can be used to force template replacement.
  """

  idToken = _auth_email()
  #_auth(target)

  with open(_get_content_file_name(target), 'r', encoding='utf-8') as f:
    content = f.read()

  #cred = credentials.Certificate(KEY_LIVE) 
  #firebase_admin.initialize_app(cred)
 
  #firebase = FirebaseApplication(REMOTE_CONFIG_URL, None)
  #result = firebase.get('/', None)

  #credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_LIVE, SCOPES)
  # Use the credentials object to authenticate a Requests session.
  #authed_session = AuthorizedSession(credentials)
  #response = authed_session.post( url=_get_remote_config_url(accessToken), data=content.encode('utf-8'), headers=headers)
  #print(response)
  
  headers = {
    'Authorization': 'Bearer ' + _get_access_token(target),
    'Content-Type': 'application/json; UTF-8'
  }
  #accessToken = _get_access_token(target);
  url = REMOTE_CONFIG_URL + '.json?auth=' + idToken
  print(url)
  resp = requests.put(url, data=content.encode('utf-8'), headers=headers)
  print(resp)
  if resp.status_code == 200:
    print('Database update has been published.')
  else:
    print('Unable to publish database update.')
    print(resp.text)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--action')
  parser.add_argument('--etag')
  parser.add_argument('--version')
  parser.add_argument('--target', default='LIVE', const='LIVE', nargs='?', choices=['LIVE', 'SANDBOX', 'DEV'], help = 'Target LIVE or SANDBOX')
  args = parser.parse_args()

  if args.action and args.action == 'get' and args.target:
    _get(args.target)
  elif args.action and args.action == 'publish' and args.target:
    _publish(args.target)
  elif args.action and args.action == 'versions' and args.target:
    _listVersions(args.target)
  elif args.action and args.action == 'rollback' and args.version and args.target:
    _rollback(args.version, args.target)
  else:
    print('''Invalid command. Please use one of the following commands:
    	python3 remote.py --action=get
python3 remote.py --action=get --target SANDBOX
python3 remote.py --action=publish --etag=<LATEST_ETAG>
python3 remote.py --action=publish --target SANDBOX --etag=<LATEST_ETAG>
python3 remote.py --action=versions
python3 remote.py --action=rollback --version=<TEMPLATE_VERSION_NUMBER>''')



if __name__ == '__main__':
  main()
