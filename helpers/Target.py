from enum import Enum

class Target(Enum):
	BestPractiseIndustry = 'BPI'
	BuildingSolutionsUK = 'BS'
	BuildingAndConstructionReview = 'BCR'
	BuildingAndFaciltiesNews = 'BFN'
	BusinessAndIndustryToday = 'BAIT'
	FoodAndDrinkMatters = 'FDM'
	IndustrialProcessNews = 'IPN'
	ProductAndServicesReview = 'PSR'
	SolutionsPublishing = 'SP'
	TradexNews = 'TN'

def getTarget(enum):
	return Target(enum)