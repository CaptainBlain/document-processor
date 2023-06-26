import os
import pathlib
import sys

from helpers.Target import Target
from helpers.Target import getTarget


SCOPES = ["https://www.googleapis.com/auth/firebase.database"]
DATABASE_DIRECTORY = '/database/'

def getCurrentPath():
  return pathlib.Path(__file__).parent.resolve()

def getServicesDirectory():
    return str(getCurrentPath()) + '/services/'
  
def getPdfCellJson(target, thumbnail, pdfLink, issue):
  json = {}
  if target == Target.BestPractiseIndustry:
    json = {
      "CellType" : "PDFCell",
      "Description" : "The team at Best Practice Industry UK has been working extremely hard to bring you an issue that is full of innovative and exhilarating companies and we are very excited to share their success and achievements with you.",
      "SortOrder" : "2",
      "ThumbnailImage" : thumbnail,
      "Title" : "Best Practice " + issue,
      "pdfLink" : pdfLink
    }
  elif target == Target.BuildingSolutionsUK:
    json =  {
      "CellType" : "PDFCell",
      "Description" : "The team at Building Solutions UK has been working extremely hard to bring you an issue that is full of innovative and exhilarating companies and we are very excited to share their success and achievements with you.",
      "SortOrder" : "",
      "ThumbnailImage" : thumbnail,
      "Title" : "Building Solutions UK " + issue,
      "pdfLink" : pdfLink
    }
  elif target == Target.BuildingAndConstructionReview:
    json = {
      "CellType" : "PDFCell",
      "Description" : "The team at Building & Construction Review UK has been working extremely hard to bring you an issue that is full of innovative and exhilarating companies and we are very excited to share their success and achievements with you.",
      "SortOrder" : "",
      "ThumbnailImage" : thumbnail,
      "Title" : "Building & Construction Review UK " + issue,
      "id" : "1",
      "pdfLink" : pdfLink
    }
  elif target == Target.BuildingAndFaciltiesNews:
    json = {
      "CellType" : "PDFCell",
      "Description" : "The team at Building and Facilities News has been working extremely hard to bring you an issue that is full of innovative and exhilarating companies and we are very excited to share their success and achievements with you.",
      "SortOrder" : "",
      "ThumbnailImage" : thumbnail,
      "Title" : "Building & Facilities News Issue " + issue,
      "pdfLink" : pdfLink
    }
  elif target == Target.BusinessAndIndustryToday:
    json = {
      "CellType" : "PDFCell",
      "Description" : "The team at Business and Industry today has been working extremely hard to bring you an issue that is full of innovative and exhilarating companies and we are very excited to share their success and achievements with you.",
      "SortOrder" : "",
      "ThumbnailImage" : thumbnail,
      "Title" : "Business and Industry Today Issue " + issue,
      "pdfLink" : pdfLink
    }
  elif target == Target.FoodAndDrinkMatters:
    json =  {
      "CellType" : "PDFCell",
      "Description" : "The team at Food & Drink Matters has been working extremely hard to bring you an issue that is full of innovative and exhilarating companies and we are very excited to share their success and achievements with you.",
      "SortOrder" : "",
      "ThumbnailImage" : thumbnail,
      "Title" : "Food & Drink Matters Issue " + issue,
      "pdfLink" : pdfLink
    }
  elif target == Target.IndustrialProcessNews:
    json = {
      "CellType" : "PDFCell",
      "Description" : "The team at Industrial Process News today has been working extremely hard to bring you an issue that is full of innovative and exhilarating companies and we are very excited to share their success and achievements with you.",
      "SortOrder" : "",
      "ThumbnailImage" : thumbnail,
      "Title" : "Industrial Process News Issue " + issue,
      "pdfLink" : pdfLink
    }
  elif target == Target.ProductAndServicesReview:
    json = {
      "CellType" : "PDFCell",
      "Description" : "The team at Products & Services Review has been working extremely hard to bring you an issue that is full of innovative and exhilarating companies and we are very excited to share their success and achievements with you.",
      "SortOrder" : "",
      "ThumbnailImage" : thumbnail,
      "Title" : "Products & Services Review Issue " + issue,
      "pdfLink" : pdfLink
    }
  elif target == Target.SolutionsPublishing:
    json = {
      "CellType" : "PDFCell",
      "Description" : "I hope you enjoy reading this issue as much as we have enjoyed bringing it to you. Happy reading and we hope to see you for the next edition!",
      "SortOrder" : "",
      "ThumbnailImage" : thumbnail,
      "Title" : "Building Update " + issue,
      "pdfLink" : pdfLink
    }
  elif target == Target.TradexNews:
    json = {
      "CellType" : "PDFCell",
      "Description" : "The team at Tradex News has been working extremely hard to bring you an issue that is full of innovative and exhilarating companies and we are very excited to share their success and achievements with you.",
      "SortOrder" : "",
      "ThumbnailImage" : thumbnail,
      "Title" : "Tradex News Issue " + issue,
      "pdfLink" : pdfLink
    }
  elif target == Target.IndustryUpdate:
    json = {
      "CellType" : "PDFCell",
      "Description" : "The team at Industry Update has been working extremely hard to bring you an issue that is full of innovative and exhilarating companies and we are very excited to share their success and achievements with you.",
      "SortOrder" : "",
      "ThumbnailImage" : thumbnail,
      "Title" : "Industry Update Issue " + issue,
      "pdfLink" : pdfLink
    }
  return json
    

def getStorageBucket(target):
  bucket = ''
  if target == Target.BestPractiseIndustry:
    bucket = 'best-practice-industry.appspot.com'
  elif target == Target.BuildingSolutionsUK:
    bucket = 'building-solutions-uk.appspot.com'
  elif target == Target.BuildingAndConstructionReview:
    bucket = 'buildingandconstructionreview.appspot.com'
  elif target == Target.BuildingAndFaciltiesNews:
    bucket = 'buildingandfacilitiesnews.appspot.com'
  elif target == Target.BusinessAndIndustryToday:
    bucket = 'businessandindustrytoday.appspot.com'
  elif target == Target.FoodAndDrinkMatters:
    bucket = 'foodanddrinkmatters.appspot.com'
  elif target == Target.IndustrialProcessNews:
    bucket = 'industrialprocessnews.appspot.com'
  elif target == Target.ProductAndServicesReview:
    bucket = 'productservicesreview.appspot.com'
  elif target == Target.SolutionsPublishing:
    bucket = 'solutionspublishing-94e4b.appspot.com'
  elif target == Target.TradexNews:
    bucket = 'tradexnews-79603.appspot.com'
  elif target == Target.IndustryUpdate:
    bucket = 'industry-update-f17a9.appspot.com'
  return bucket 


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
  elif target == Target.IndustryUpdate:
    fileName = os.path.join(getServicesDirectory(), 'industry-update-service-account.json')
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
  elif target == Target.IndustryUpdate:
    savePath = os.path.join(getContentPathName(target), 'iu-realtime-database.json') 
  return savePath  








