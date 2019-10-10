from setup.Venue import *
from setup.Military import Military
from setup.StadiumPower import Stadium, PowerPlant, Embassy

# Initial setup requiring user input airspace category and venue name
def setup():
	print("loading setup")
	loadFromPrev = input("Would you like to use the previous configuration? (y/n): ")
	if loadFromPrev == 'y' or loadFromPrev == 'Y':
		return loadConfig()
	elif loadFromPrev == 'n' or loadFromPrev == 'N':
		airspace = askForCategory()
		# airspace.askForState() # Currently slows down program
		airspace.askForVenue()
		airspace.askForAltitude()
		airspace.setPolygon()
		writeConfig(airspace)
		return airspace
	else:
		print("Please type in y or n")

# Prompt user to enter desired airspace category
def askForCategory():
	while (True):
		print ("1 - Controlled Airspace")
		print ("2 - Military Base")
		print ("3 - National Park")
		print ("4 - Prison")
		print ("5 - Stadium")
		print ("6 - Power Plant")
		print ("7 - Foreign Embassy")
		user_input = (input("Enter an airspace category: ")).lower()
		user_input = user_input.strip()
		airspace = setCategory(user_input)
		if airspace != None:
			#print(airspace.shapeData['features'][50])
			return airspace
		else:
			print("That category is unavailable. Please try again")
	return airspace

# Creates proper object relating to user's selected airspace category
def setCategory(user_input):
	if user_input == "1" or user_input == "faa controlled airspace" or user_input == "FAA Controlled Airspace" or user_input == "airport":
		airspace = FAA()
	elif user_input == "2" or user_input == "military base" or user_input == "Military Base":
		airspace = Military()
	elif user_input == "3" or user_input == "national park" or user_input == "National Park":
		airspace = NationalPark()
	elif user_input == "4" or user_input == "prison" or user_input == "prisons" or user_input == "Correctional Facility":
		airspace = Prison()
	elif user_input == "5" or user_input == "stadium" or user_input == "Stadium":
		airspace = Stadium()
	elif user_input == "6" or user_input == "power plant" or user_input == "power plants" or user_input == "Power Plant":
		airspace = PowerPlant()
	elif user_input == "7" or user_input == "Foreign Embassy":
		airspace = Embassy()
	else:
		airspace = None
	return airspace

# Load previous configuration stored in text file
def loadConfig():
	file = open("drone_tracker_config.txt", "r")
	category = (file.readline()).lower().strip()
	airspace = setCategory(category)
	#print(type(airspace))
	venue = (file.readline()).lower().rstrip()
	airspace.setVenue(venue)
	alt = (file.readline()).lower().rstrip()
	airspace.setAltitude(alt)
	airspace.setPolygon()
	file.close()
	return airspace

# Write configuration to a text file
def writeConfig(airspace):
	file = open("drone_tracker_config.txt", "w")
	config = airspace.getUserConfig()
	for i in config:
		file.write(i + "\n")
	file.close() 





