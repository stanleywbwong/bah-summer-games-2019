from setup.locator_functions import *
import json

# Base class of FAA, NationalPark, Prison, Stadium, Powerplant, and Military
class Venue:
	def __init__(self, filePath, nameKey, isGeoJSON = False):
		"""Instantiates a Venue object.
		filePath = the file path to the class's corresponding shape file
		nameKey = name key that stores the name of the venue
		"""
		self.shapeFilePath = filePath
		self.nameKey = nameKey
		if isGeoJSON:
			with open(filePath) as f:
				self.shapeData = json.load(f)
		else:
			# Converts shape file into GeoJSON format
			self.shapeData = dataFormat(shapefile.Reader(filePath))
		# List that stores user inputs in the order: user selected category, venue name, altitude, user authorization
		self.userConfig = [] 

	def askForVenue(self):
		""" 
		Prompts the user to enter the name of the desired venue.
		Function then calls setVenue.
		"""
		while (True):
			userVenue = (input("Enter venue name: ")).lower()
			userVenue = userVenue.strip()
			if (self.setVenue(userVenue)):
				break
			else:
				print("Could not find venue. Did you mean: ")
				print(self.possible)

	def setVenue(self, userVenue):
		"""
		Calls searchVenue(userVenue) and returns True if the venue has been found.
		Sets self.venue to the appropriate venue data if the venu exists.
		userVenue = the name of the user's desired venue
		"""
		print("Searching for venue")
		venueAirspace = self.searchVenue(userVenue)
		if venueAirspace != None:
			#print(venueAirspace)
			self.venue = venueAirspace
			self.userConfig.append(userVenue)
			print("Venue set")
			return True
		else:
			return False

	def searchVenue(self, venue):
		""" 
		Searches through geoJSON data for the user-inputted venue name and returns the data associated with that venue.
		If the venue does not exist, then function returns None and also sets a list of possible venues.
		venue = the name of the user's desired venue
		"""
		self.possible = [] #reset list of possible venues
		for i in range(len(self.shapeData['features'])):
			# Searches for the exact venue name
			if venue == (self.shapeData['features'][i]['properties'][self.nameKey]).lower(): 
				venueAirspace = self.shapeData['features'][i]
				return venueAirspace
			# If the user-inputted name is not found, then self.possible is assigned a list of possible venue names
			elif venue in (self.shapeData['features'][i]['properties'][self.nameKey]).lower():
				self.possible.append(self.shapeData['features'][i]['properties'][self.nameKey])

	def getVenue(self):
		"""Returns the data associated with the venue"""
		return self.venue

	def getShapeData(self):
		"""Returns the geoJSON data associated with the class"""
		return self.shapeData

	def setPolygon (self):
		"""Creates a polygon of the venue airspace (stored in self.polygon) given the venue's coordinates."""
		print("Creating polygon")
		venuePoints = self.venue['geometry']['coordinates']
		venuePolygons = createPolygon(venuePoints)
		self.polygon = venuePolygons
		print("Polygon created")

	def getCoords (self):
		"""Returns the coordinates of the venue."""
		return self.venue['geometry']['coordinates']

	def getPolygon(self):
		"""Returns the polygon of the venue airspace."""
		return self.polygon

	def getUserConfig(self):
		"""Returns the list of the user's inputs."""
		return self.userConfig

	def askForAltitude(self):
		"""Asks user to enter an altitude so if the drone is below that altitude,
		then it is considered within the venue's airspace."""
		while True:
			userAlt = input("Enter desired altitude: ")
			if (self.setAltitude(userAlt)):
				break
			else:
				print("Please enter a valid number")

	def setAltitude(self, userAlt):
		"""Stores the user-inputted altitude and returns True if the altitude is a number.
		userAlt = user's desired altitude
		"""
		if userAlt.isdigit():
			self.altitude = float(userAlt)
			self.userConfig.append(userAlt)
			return True
		else:
			return False

	def getAltitude(self):
		"""Returns the user's altitude."""
		return self.altitude

	def getPossible(self):
		"""Returns the list of possible venue names that contains the user-inputted venue name."""
		return self.possible

# Class representing FAA controlled airpsace area, mostly airports
class FAA(Venue):
	def __init__(self):
		"""Instantiates an FAA object by calling Venue's constructor."""
		super().__init__("shp/FAA_UAS_FacilityMap_Data_V2.shp", 'ARPT_COUNT')
		self.userConfig.append("faa controlled airspace")

	def askForVenue(self):
		"""Asks user to enter IATA code for desired airport."""
		while (True):
			userVenue = (input("Enter IATA code for airports: ")).lower()
			userVenue = userVenue.strip()
			if (self.setVenue(userVenue)):
				break
			else:
				print("Could not find airport.")

	def setVenue(self, userVenue):
		"""Returns True if user airport is found and stores its associated data into self.venue.
		userVenue = IATA code of user's desired airport
		"""
		print("Searching for venue")
		venueAirspace = self.searchVenue(userVenue.lower().strip())
		if venueAirspace != []:
			#print(venueAirspace)
			self.venue = venueAirspace
			self.userConfig.append(userVenue)
			print("Venue set")
			return True
		else:
			return False

	def searchVenue(self, venue):
		"""Searches through geoJSON data for the specified airport and returns a list of all data associated with it.
		Note: Airports in the FAA shape file data have multiple geoJSON data entries associated with each.
		venue = IATA code of user's desired airport
		"""
		venueAirspace = [] #reset list of possible venues
		for i in range(len(self.shapeData['features'])):
			#print("af")
			if venue == (self.shapeData['features'][i]['properties'][self.nameKey]).lower():
				venueAirspace.append(self.shapeData['features'][i])
		return venueAirspace

	def setPolygon (self):
		"""Creates a list of polygons of the airport airspace (stored in self.polygon) given the airport's coordinates."""
		print("Creating polygon")
		venuePolygons = []
		for i in range(len(self.venue)):
			venuePolygons.append(createPolygon(self.venue[i]['geometry']['coordinates']))
		self.polygon = venuePolygons
		print("Polygon created")

	def getCoords(self):
		"""Returns a list of the airport's coordinates."""
		coords = []
		for i in range(len(self.venue)):
			coords.append(self.venue[i]['geometry']['coordinates'])
		return coords

# Class representing a national park airspace
# Note: There are coordinate formatting errors with several national parks
class NationalPark(Venue):
	def __init__(self):
		"""Instantiates a NationalPark object by calling Venue's constructor."""
		super().__init__("shp/National_Park_Service__Park_Unit_Boundaries.geojson", 'UNIT_NAME', True)
		self.userConfig.append("national park")

# Class representing a prison airspace
class Prison(Venue):
	def __init__(self):
		"""Instantiates a Prison object by calling Venue's constructor."""
		super().__init__("shp/Prison_Boundaries.dbf", 'FACILITYID')
		self.userConfig.append("prison")