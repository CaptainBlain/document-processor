import argparse
import requests

import json
import random

from auth_dp.target import get_target


BASE_URL = "https://identitytoolkit.googleapis.com/v1/accounts"
SIGN_UP_URL = BASE_URL + ":signUp"

def get_API_key(target):
  key = ''
  if target == Target.BestPractiseIndustry:
    key = 'AIzaSyCay3PJl05C1f3k_3eWUfMoBneURSToXoA'
  elif target == Target.BuildingSolutionsUK:
    key = 'AIzaSyCukSdk4gtsCdXN819VQ6iUn9fUl5kQN2Q'
  elif target == Target.BuildingAndConstructionReview:
    key = 'AIzaSyD6-tePneOvxgyG36fL8dI7WyIU8-NYvas'
  elif target == Target.BuildingAndFaciltiesNews:
    key = 'AIzaSyDzik_hZ0sTyLOCtY-5uKNycJGbc_NVTs4'
  elif target == Target.BusinessAndIndustryToday:
    key = 'AIzaSyAqkUaaRHT7Rc96zt-WQu7WVdPp4WtpCJA'
  elif target == Target.FoodAndDrinkMatters:
    key = 'AIzaSyA0DZBHwr2x5kYYYeVbVhCmqH1P1EtTDis'
  elif target == Target.IndustrialProcessNews:
    key = 'AIzaSyDTkh6fxJTPwkFmedYFUjtMf4wzl688fMs'
  elif target == Target.ProductAndServicesReview:
    key = 'AIzaSyDbVkE0fn-BYomErppt3Tr6cKBk9Acp8Oo'
  elif target == Target.SolutionsPublishing:
    key = 'AIzaSyAKI_4CDCMed9XDb6HcyJHEIwNrcjAkw9I'
  elif target == Target.TradexNews:
    key = 'AIzaSyC1jM7avSGL6ndDqhLFO-TWiLe7kHMa1j0'
  return key 

def get_auth_id_token_for_new_user(target):

  url = SIGN_UP_URL + "?key=" + get_API_key(target)
  ranno = random.randint(100000, 999999999)
  payload = json.dumps({
    "email": "blain.ellis+" + str(ranno) + "@gmail.com",
    "password": "PASSWORD",
    "returnSecureToken": True
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  data = response.json()
  idToken = data.get('idToken')
  return idToken
