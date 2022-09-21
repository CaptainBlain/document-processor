import os
import pathlib
import sys

# from realtime_database_worker.helpers.Target import Target
# from realtime_database_worker.helpers.Target import getTarget

from helpers.Target import Target
from helpers.Target import getTarget

SCOPES = ["https://www.googleapis.com/auth/firebase.database"]
DATABASE_DIRECTORY = '/database/'

def getCurrentPath():
  return pathlib.Path(__file__).parent.resolve()

def getServicesDirectory():
    return str(getCurrentPath()) + '/realtime_database_worker/services/'
  
def getContentPathName(target):
  pathName = str(getCurrentPath())
  if target == Target.BestPractiseIndustry:
    pathName = pathName + DATABASE_DIRECTORY + '/BPI/'
  elif target == Target.BuildingSolutionsUK:
    pathName = pathName + DATABASE_DIRECTORY + '/BS/'
  elif target == Target.BuildingAndConstructionReview:
    pathName = pathName + DATABASE_DIRECTORY + '/BCR/'
  elif target == Target.BuildingAndFaciltiesNews:
    pathName = pathName + DATABASE_DIRECTORY + '/BFN/'
  elif target == Target.BusinessAndIndustryToday:
    pathName = pathName + DATABASE_DIRECTORY + '/BAIT/'
  elif target == Target.FoodAndDrinkMatters:
    pathName = pathName + DATABASE_DIRECTORY + '/FDM/'
  elif target == Target.IndustrialProcessNews:
    pathName = pathName + DATABASE_DIRECTORY + '/IPN/'
  elif target == Target.ProductAndServicesReview:
    pathName = pathName + DATABASE_DIRECTORY + '/PSR/'
  elif target == Target.SolutionsPublishing:
    pathName = pathName + DATABASE_DIRECTORY + '/SP/'
  elif target == Target.TradexNews:
    pathName = pathName + DATABASE_DIRECTORY + '/TN/'
  os.makedirs(os.path.dirname(pathName), exist_ok=True)
  return pathName

def getRemoteConfigUrl(target):
  fileName = ''
  if target == Target.BestPractiseIndustry:
    fileName = 'https://best-practice-industry.firebaseio.com/'
  elif target == Target.BuildingSolutionsUK:
    fileName = 'https://building-solutions-uk.firebaseio.com/'
  elif target == Target.BuildingAndConstructionReview:
    fileName = 'https://buildingandconstructionreview.firebaseio.com/'
  elif target == Target.BuildingAndFaciltiesNews:
    fileName = 'https://buildingandfacilitiesnews.firebaseio.com/'
  elif target == Target.BusinessAndIndustryToday:
    fileName = 'https://businessandindustrytoday.firebaseio.com/'
  elif target == Target.FoodAndDrinkMatters:
    fileName = 'https://foodanddrinkmatters.firebaseio.com/'
  elif target == Target.IndustrialProcessNews:
    fileName = 'https://industrialprocessnews.firebaseio.com/'
  elif target == Target.ProductAndServicesReview:
    fileName = 'https://productservicesreview-default-rtdb.firebaseio.com/'
  elif target == Target.SolutionsPublishing:
    fileName = 'https://solutionspublishing-94e4b.firebaseio.com/'
  elif target == Target.TradexNews:
    fileName = 'https://tradexnews-79603.firebaseio.com/'
  return fileName 


def getKey(target):
  fileName = ''
  if target == Target.BestPractiseIndustry:
    fileName = os.path.join(getServicesDirectory(), 'best-practice-industry-account.json')
  elif target == Target.BuildingSolutionsUK:
    fileName = os.path.join(getServicesDirectory(), 'building-solutions-uk-account.json')
  elif target == Target.BuildingAndConstructionReview:
    fileName = os.path.join(getServicesDirectory(), 'buildingandconstructionreview-account.json')
  elif target == Target.BuildingAndFaciltiesNews:
    fileName = os.path.join(getServicesDirectory(), 'buildingandfacilitiesnews-account.json')
  elif target == Target.BusinessAndIndustryToday:
    fileName = os.path.join(getServicesDirectory(), 'bait-service-account.json')
  elif target == Target.FoodAndDrinkMatters:
    fileName = os.path.join(getServicesDirectory(), 'foodanddrinkmatters-account.json')
  elif target == Target.IndustrialProcessNews:
    fileName = os.path.join(getServicesDirectory(), 'industrialprocessnews-account.json')
  elif target == Target.ProductAndServicesReview:
    fileName = os.path.join(getServicesDirectory(), 'productservicesreview-account.json')
  elif target == Target.SolutionsPublishing:
    fileName = os.path.join(getServicesDirectory(), 'solutionspublishing-account.json')
  elif target == Target.TradexNews:
    fileName = os.path.join(getServicesDirectory(), 'tradexnews-account.json')
  return fileName 


def getContentFileName(target):

  savePath = ''
  if target == Target.BestPractiseIndustry:
    savePath = os.path.join(getContentPathName(target), 'bpi-realtime-database.json') 
  elif target == Target.BuildingSolutionsUK:
    savePath = os.path.join(getContentPathName(target), 'bsuk-realtime-database.json') 
  elif target == Target.BuildingAndConstructionReview:
    savePath = os.path.join(getContentPathName(target), 'bcr-realtime-database.json') 
  elif target == Target.BuildingAndFaciltiesNews:
    savePath = os.path.join(getContentPathName(target), 'bfn-realtime-database.json') 
  elif target == Target.BusinessAndIndustryToday:
    savePath = os.path.join(getContentPathName(target), 'bait-realtime-database.json') 
  elif target == Target.FoodAndDrinkMatters:
    savePath = os.path.join(getContentPathName(target), 'fdm-realtime-database.json') 
  elif target == Target.IndustrialProcessNews:
    savePath = os.path.join(getContentPathName(target), 'ipn-realtime-database.json') 
  elif target == Target.ProductAndServicesReview:
    savePath = os.path.join(getContentPathName(target), 'psr-realtime-database.json') 
  elif target == Target.SolutionsPublishing:
    savePath = os.path.join(getContentPathName(target), 'sp-realtime-database.json') 
  elif target == Target.TradexNews:
    savePath = os.path.join(getContentPathName(target), 'tn-realtime-database.json') 
  return savePath  








