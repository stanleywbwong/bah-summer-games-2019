from setup.setup_locator import *
print("loading functions")
# --------
# Shapefile Transformations
# ====

def getShapes (shp):
    polygon = shp.shapes()  #turns shapefile format into a shape object
    shpfilePoints = [ shape.points for shape in polygon ] #extracts vertices from shape object and puts it into a list format (necessary for within command)
    return shpfilePoints

#grabs the verticies of the shape and converts it to a polygon
def createPolygon(shapePoints):
    masterPoly = []
    if shapePoints == 'airspacePoints': #returns only four verticies for airspace data, w/o this the polygon fxn wouuld get confused
        for point in shapePoints:
            masterPoly.append(Polygon(point[:4]))
    else:
        for point in shapePoints:
            masterPoly.append(Polygon(point)) 
    return masterPoly


# Function Definitions

#some shapefiles only had 2 vertices, this function removes those
newShapeList = []
def remove(shapeList):
    for shape in shapeList:
        if len(shape) >3:
            newShapeList.append(shape)
    return newShapeList


#This function creates a buffer zone around a given coordinate pair with a radius of one mile
#To be used for stadium and power plant shapefiles, as we are only given a centerpoint for these features
proj_wgs84 = pyproj.Proj(init='epsg:4326')
def geodesic_point_buffer(lat, lon, km):
    # Azimuthal equidistant projection - all points on map are proportionally correct distances from the center point 
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
        proj_wgs84)
    buf = Point(0, 0).buffer(km * 1609.34)  # distance in meters
    return transform(project, buf).exterior.coords[:]


def drawRadius(shapePoints, radius): 
    radiusList = []
    for point in shapePoints:
        radiusList.append(geodesic_point_buffer(point[0][1], point[0][0], radius))
    return radiusList

# Formats the shapefile data into GeoJSON input
def dataFormat (shapefile):
    shapeData = shapefile.__geo_interface__
    return shapeData

# Separates out the altitude from the parameter
def removeAltitude(tuples):
    alt = tuples[-1]
    new_tup = tuples[:-1]
    return [new_tup, alt]


#need to reverse it, as detection function doesn't work with (lat,long), works with (y,x)
def Reverse(tuples): 
    new_tup = tuples[::-1] 
    return new_tup 

# Determine if point within polygon
def detection(point, polygons, shapeData, altitude):
    ptList = removeAltitude(point)
    #print(ptList)
    pt = Point((ptList[0]))
    for i in range(len(polygons)):
        # If polygons is a list, need to index another level to access actual polygon object
        if isinstance(polygons[i], list):
            if pt.within(polygons[i][0]) == True:
                if ptList[1] <= altitude:
                    return True
        else:
            if pt.within(polygons[i]) == True:
                if ptList[1] <= altitude:
                    return True
    return False


'''
def locate(point, polygon, shapeData):

    #will detect if if drone is found in any of these restricted airspaces
    airspaceLocationData = pd.DataFrame(detection(point, polygon, shapeData))

    dataList = [shapeData]

    locationData = locationSearch(dataList)
    locationData = locationData.transpose()
    locationData = locationData.drop(['type', 'geometry'])
    locationData

    geolocator = Nominatim()
    location = geolocator.reverse(gpsInput)
    print( location.address)

#if the point is in one of these spaces, will return data on it
def locationSearch (dataList):
    for i in dataList:
        if len(i) > 0:
            return i
'''
