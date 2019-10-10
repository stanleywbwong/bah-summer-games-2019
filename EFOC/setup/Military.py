from setup.Venue import *

# Class representing a military base airspace
class Military(Venue):
	def __init__(self):
		"""Instantiates a Military object by calling Venue constructor."""
		super().__init__("shp/Military_Bases.shp", 'COMPONENT')
		self.userConfig.append("military base")

	def setPolygon (self):
		"""Creates the polygon of the military base airspace based on its coordinates.
		getTuple(venuePoints) is called to format the coordinates properly.
		"""
		print("Creating polygon")
		venuePoints = self.venue['geometry']['coordinates']
		venuePoints = self.getTuple(venuePoints)
		#print(venuePoints)
		venuePolygons = createPolygon(venuePoints)
		self.polygon = venuePolygons

	def getPolygon(self):
		"""Returns the military base's polygon."""
		return self.polygon

	def getTuple(self, pointTuple):
		"""Formats the coordinates so createPolygon() can process them and returns a list of coordinate tuples.
		This is needed because the coordinates of military base geoJSON data is formatted as tuples within 
		one large tuple. 
		
		pointTuple = the large tuple which contains all the coordinates of a military base airspace
		
		Note: Error wth Los Angeles AFB
		"""
		tupleList = []
		bigTuple = pointTuple[0][0]
		newTuple = [x for x in bigTuple if x != None]
		tupleList.append(newTuple)
		return tupleList