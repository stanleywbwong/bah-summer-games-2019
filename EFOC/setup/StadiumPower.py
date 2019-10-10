from setup.Venue import *

# Class representing a stadium's airspace
class Stadium(Venue):
	def __init__(self):
		"""Instantiates a Stadium object by calling Venue constructor."""
		super().__init__("shp/Major_Sport_Venues.shp", 'VENUEID')
		self.userConfig.append("stadium")

	def __init2__(self, filepath, nameKey, isGeoJSON):
		"""Second constructor which instantiates a PowerPlant object by calling Venue's constructor."""
		super().__init__(filepath, nameKey, isGeoJSON)

	def setPolygon (self):
		"""Creates the stadium airspace polygon with a 0.5 mile radius of points around the center of the stadium.
		Note: Both stadium and powerplant data only include a single central coordinate point which cannot
		be used to create a polygon.
		"""
		venuePoints = self.venue['geometry']['coordinates']
		venuePoints = self.get3List(venuePoints)
		#print(venuePoints)
		#Need to call drawRadius to obtain a circle of points around the center of the stadium
		venuePolygons = createPolygon(drawRadius(venuePoints, 0.25))
		self.polygon = venuePolygons

	def getPolygon(self):
		"""Returns the polygon."""
		return self.polygon

	def get3List(self, pointTuple):
		"""Converts a tuple to a triple nested list which is compatible with drawRadius()
		and returns that triple nested list.

		pointTuple = tuple of the stadium's coordinates
		"""
		pointList = []
		pointList2 = []
		pointList3 = []
		for i in range(len(pointTuple)):
			pointList.append(pointTuple[i])
		pointList2.append(pointList)
		pointList3.append(pointList2)
		return pointList3 

# Class which inherits from Stadium and represents a power plant airspace
# PowerPlant also needs to call drawRadius()
class PowerPlant(Stadium):
	def __init__(self):
		"""Instantiates a PowerPlant object by calling a Stadium constructor 
		which then calls the Venue constructor.
		"""
		super().__init2__("shp/Power_Plants.shp", 'PLANT_CODE', False)
		self.userConfig.append("power plant")

	def setPolygon (self):
		"""Creates the powerplant airspace polygon with a 0.9 mile radius of points around the center of the powerplant.
		"""
		venuePoints = self.venue['geometry']['coordinates']
		venuePoints = self.get3List(venuePoints)
		#print(venuePoints)
		#Need to call drawRadius to obtain a circle of points around the center of the stadium
		venuePolygons = createPolygon(drawRadius(venuePoints, 0.9))
		self.polygon = venuePolygons


class Embassy(Stadium):
	def __init__(self):
		"""Instantiates an Embassy object by calling Venue's constructor."""
		super().__init2__("shp/Embassies.geojson", 'EMB_TITLE', True)
		self.userConfig.append("Embassy")


	def setPolygon (self):
		"""Creates the embassy airspace polygon with a 0.12 mile radius of points around the center of the embassy.
		"""
		venuePoints = self.venue['geometry']['coordinates']
		venuePoints = self.get3List(venuePoints)
		#print(venuePoints)
		#Need to call drawRadius to obtain a circle of points around the center of the embassy
		venuePolygons = createPolygon(drawRadius(venuePoints, 0.10))
		self.polygon = venuePolygons