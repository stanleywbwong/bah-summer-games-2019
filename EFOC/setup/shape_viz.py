#from input_location import setup
from shapely.geometry import Polygon
from ast import literal_eval
from setup.Venue import *
import simplekml


def format(testPoly, setup):
	if isinstance(setup, FAA):
		newCoordList = []
		airCoordList = setup.getCoords()
		for i in range(len(airCoordList)):
			for j in range(len(airCoordList[0])):
				for k in range(len(airCoordList[0][0])):
					#print(airCoordList[i][j][k])
					newCoordList.append(airCoordList[i][j][k])
		return newCoordList
	else: #for everything else
		coords = (testPoly[0].exterior.coords)
		coords = list(coords)
		return coords


def outerBound(coords, alt):
	outerList = []
	innerInner = []
	for coordPair in coords:
		#coordPair = coordPair[0] #comment out for airspace, need to have it for other shapefiles
		coordPair = str(coordPair)
		coordPair = (str(coordPair).strip(')')+','+str(alt)+')')
		coordPair = literal_eval(coordPair)
		outerList.append(coordPair)
	return outerList

def innerBound(coords, alt):
	innerList = []
	for coordPair in coords:
		#coordPair = coordPair[0] #comment out for airspace, need to have it for other shapefiles
		coordPair = str(coordPair)
		coordPair = (str(coordPair).strip(')')+','+str(alt)+')')
		coordPair = literal_eval(coordPair)
		innerList.append(coordPair)
	return innerList


def createBounds(outerBoundary, innerBoundary):
	kml = simplekml.Kml()
	#Create a polygon with specified outer and inner boundary
	#Coordinates in format (longitude, latitude, altitude)
	pol = kml.newpolygon(name = "Space", 
			    outerboundaryis = outerBoundary,
	                    innerboundaryis = innerBoundary
			    )
	#Extrude the polygon to create 3D shape
	pol.extrude = 1

	#Set polygon relative to ground
	pol.altitudemode = simplekml.AltitudeMode.relativetoground

	#Set polygon color to transparent
	pol.style.polystyle.color = '00000000'
	#pol.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.green)

	#Add outline to polygon
	pol.style.polystyle.outline = 1

	kml.save("visualization\\boundary.kml")

def clearKML(name):
	kml = simplekml.Kml()
	lin = kml.newlinestring(name = name)
	kml.save("visualization\\" + name + ".kml")

	
def drawPath(points, name):
	kml = simplekml.Kml()
	lin = kml.newlinestring(name=name, description="Drone path", coords=points)
	lin.altitudemode = simplekml.AltitudeMode.relativetoground
	lin.style.linestyle.width = 5
	lin.style.linestyle.color = simplekml.Color.blue
	kml.save("visualization\\" + name + ".kml")

def drawBox(name, location):
	kml = simplekml.Kml()
	descript = "<p><img style='max-width:250px;' img src='https://asset.conrad.com/media10/isa/160267/c1/-/en/001968169PI00/image.jpg'> <p>Drone Model: Tello EDU" + "<p>Coordinates: (%s, %s, %s)" % (location[0], location[1], location[2])
	pos = kml.newpoint(name = "UAS Intrusion Info", description = descript, coords = [(location[0], location[1], location[2])])
	pos.altitudemode = simplekml.AltitudeMode.relativetoground
	pos.style.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/caution.png"
	#pos.style.iconstyle.scale = 2
	kml.save("visualization\\" + name + ".kml")



'''
setup = FAA()
print(setup.setVenue('BED'))
setup.setPolygon()
testPoly = setup.getPolygon()
createBounds(outerBound(format(testPoly,setup),500),innerBound(format(testPoly,setup),0))
'''