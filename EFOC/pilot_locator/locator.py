#Peter Malinovsky (and some stuff added by Stan :) )
#605277
#Booz Allen Hamilton
#Summer Games 2019

import pyproj
from functools import partial
from shapely.ops import transform
import simplekml
import math
import shapely.geometry as geometry
from shapely.geometry import Point, Polygon
import threading
import time
from multiprocessing import Process
import os
from setup.shape_viz import *
import getpass


#geodesic_point_buffer
#Inputs: latitude, longitude, radium in miles
#Return: transform of gps circle from the provided input
#Disclaimer: this function was found on StackOverflow and I do not know how it works
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


#interpolate
#Inputs: list of rounded ordered coordintates in a circumference, decimal the coordinates have been rounded to
#Return: list of rounded ordered cooredinates that completely encapsulates an area to the rounded value provided
def interpolate(coords, r):
	new_coords = []
	for i in range(len(coords) - 1):
		xdiff = coords[i + 1][0] - coords[i][0]
		ydiff = coords[i + 1][1] - coords[i][1]
		v = math.pow(10, -r)
		if xdiff != 0:
			slope = ydiff / xdiff
		else:
			slope = float("inf")

		if abs(xdiff) < (1.5 * v) and abs(ydiff) < (1.5 * v):
			new_coords.append(coords[i])
		else:
			new_coords.append((coords[i][0], coords[i][1]))

			if abs(xdiff) >= (1.5 * v) and abs(slope) < 1:
				xpoints = round(xdiff / v)
				xmag = xpoints / abs(xpoints)
				xpoints = abs(xpoints)

				for j in range(1, xpoints):
					x = xmag * j * v
					temp_x = round(coords[i][0] + x, r)
					temp_y = round(coords[i][1] + (x * slope), r)
					new_coords.append((temp_x, temp_y))

			else:
				ypoints = round(ydiff / v)
				ymag = ypoints / abs(ypoints)
				ypoints = abs(ypoints)
				reverse_slope = xdiff / ydiff
				
				for j in range(1, ypoints):
					y = ymag * j * v
					temp_y = round(coords[i][1] + y, r)
					temp_x = round(coords[i][0] + (y * reverse_slope), r)
					new_coords.append((temp_x, temp_y))

	new_coords.append(coords[-1])
	return new_coords


#gridBuffer
#Inputs: center coordinate, radius of circle in miles, decimal place to round to
#Return: list of rounded ordered unique coodinates that completely encapsulates an area to the rounded value provided
def gridBuffer(coord, radius, rounding):
	t = geodesic_point_buffer(coord[0], coord[1], radius)

	points = []
	for elem in t:
		coord = (round(elem[0], rounding), round(elem[1], rounding))
		points.append(coord)

	new_points = list(dict.fromkeys(points))
	new_points.append(new_points[0])

	new_coords = interpolate(new_points, rounding)
	unique_new_coords = list(dict.fromkeys(new_coords))

	return unique_new_coords


#errorCheck
#Inputs: list of coordinates in total area pilot could be, decimal place to round to
#Return: prints if error has occured in tracing the outline, interpolating or filling in the circle
def errorCheck(new_coords, rounding):
	v = math.pow(10, -rounding)

	for i in range(len(new_coords) - 1):
		xdiff = new_coords[i][0] - new_coords[i + 1][0]
		ydiff = new_coords[i][1] - new_coords[i + 1][1]

		if xdiff > (v * 1.5) or ydiff > (v * 1.5):
			print("Error in interpolation")
			print(xdiff, ydiff)
			print(new_coords[i][0], new_coords[i + 1][0])
			print(new_coords[i][1], new_coords[i + 1][1])

#savetoKML
#Inputs: list of points to save, name of file to save to
#Return: saved file in the output folder
def savetoKML(points, name):
	kml = simplekml.Kml()
	lin = kml.newlinestring(name=name, description="A pathway in test", coords=points)
	lin.altitudemode = simplekml.AltitudeMode.relativetoground
	lin.style.linestyle.width = 1
	lin.style.linestyle.color = simplekml.Color.red
	kml.save("visualization/" + name + ".kml")

#saveGIStoKML
#Inputs: list of points to save, land class weight mask of these points, name of file to save to
#Return: saved file in the output folder
def GIStoKML(points, weights, name):

	weight_colors = {4: '88ff3399', 5: '88ff3333', 6: '88ffff33', 7: '8833ff33', 8: '8833ffff', 9: '883399ff', 10: '883333ff'}

	kml = simplekml.Kml()
	for i in range(len(points)):
	    pnt = kml.newpoint()
	    #pnt.name = str(weights[i])
	    pnt.coords = [(points[i][0], points[i][1])]
	    pntstyle = simplekml.Style()
	    pntstyle.iconstyle.color = weight_colors[weights[i]]    
	    pntstyle.iconstyle.scale = 0.5

	    pntstyle.iconstyle.icon.href = "resources\\Solid_white.png"
	    pnt.style = pntstyle
	kml.save("visualization/" + name + ".kml")
	print("Pilot location predictions available (see Google Earth)")

#fillOutline
#Inputs: center of the are to fill in, grid of points surrounding the center, decimal place to round to
#Return: list of coordinates that fills in the grid outline
#Note: this is algorithm assumes the shape it is filling in is circular to improve speed
def fillOutline(center, grid, rounding):
	v = math.pow(10, -rounding)
	fill = []
	x_mag = 1
	y_mag = 1
	new_point = (center[1], center[0])

	while new_point not in grid:
		new_point = (round(new_point[0] + (v * x_mag), rounding), round(new_point[1], rounding))

		if new_point in grid:
			x_mag = -x_mag
			new_point = findNewPoint(new_point, grid, x_mag, y_mag, rounding)

			if new_point in grid:
				if y_mag == -1:
					break
				x_mag = -1
				y_mag = -1
				new_point = (center[1], center[0])
		fill.append(new_point)

	return fill


#findNewPoint
#Helper function to fillOutline (its pretty complicated)
def findNewPoint(new_point, grid, x_mag, y_mag, rounding):
	v = math.pow(10, -rounding)
	temp = (round(new_point[0] + (v * x_mag), rounding), round(new_point[1] + (v * y_mag), rounding))

	while temp in grid:
		temp = (round(temp[0] + (v * x_mag), rounding), round(temp[1], rounding))

		if temp not in grid and (round(temp[0], rounding), round(temp[1] + (v * -y_mag), rounding)) in grid:
			return new_point
	return temp

def process_landclasses(points, landclasses):
	#Map to land class weights - READ FROM FILE LATER
	class_weights = {11: 6, 12: 6, 21: 10, 22: 9, 23: 8, 24: 7, 31: 9, 41: 4, 42: 4, 43: 4, 
					51: 8, 52: 9, 71: 10, 72: 9, 73: 10, 74: 10, 81: 10, 82: 8, 90: 5, 95: 5}

	#Read in land classes of original points from landclasses.txt
	weight_mask = []
	fp = open(landclasses, "r")
	lines = fp.readlines()
	for line in lines:
		weight_mask.append(class_weights[int(line.strip('\n'))]) #Add weight to weight list by accessing dictionary above

	GIStoKML(points, weight_mask, "GIS_Layer")


#Operator class that holds the area where the drone pilot could potentially be located
#Functions to use:
# Constructor: radius to draw around drone, decimal to round to (3 or 4), threads to use (usually 2 or 4), area to remove as potential space for the pilot to be (fenced area)
# run: coordinate drone is seen at
#  -run should be called for each coordinate the drone is seen at
#  -When run is called the first time it will take a noticable delay before all of the points can be populated
#  -Intial iterations will lag behind the real time position of the drone, but as the area gets smaller the program will run in real time
#  -The reduction of points takes place in a different thread and should not adversely effect the performance of the main program
#  -An attempt to speed up the processing of points using multiprocessing to compute bounding space in parallel but was never functional, the current program uses multithreading 
# which does not allow for true parallel computing to take place but has been observed to provided a noticable improvement in latency and dropped data packets
#  -To stay in time with the real-time location of the drone, data packets close together will be dropped to improve processing time. This choice was made on the basis that coordinates
# close in time will be close in position and will not maximize the number of points to eliminate from where the drone pilot could be
class Operator():
	def __init__(self, radius, rounding, max_threads = 4, restricted_area = None):
		self.first_time = True
		self.total_area = []
		self.radius = radius
		self.rounding = rounding
		if restricted_area != None:
			self.restricted_area = restricted_area[0]
		else:
			self.restricted_area = None
		self.thread = 0
		self.active_threads = 0
		self.max_threads = max_threads
		self._debug = False
		self.drop_count = 0
		savetoKML(self.total_area, "changing_area")

	def debug(self):
		self._debug = True

	def start(self, coord):

		grid_outline = gridBuffer(coord, self.radius, self.rounding)
		errorCheck(grid_outline, self.rounding)
		fill = fillOutline(coord, grid_outline, self.rounding)
		self.total_area = grid_outline + fill
		self.good = [1] * len(self.total_area)

		if self.restricted_area != None:
			self.removeRestrictedArea()

		savetoKML(self.total_area, "changing_area")


	def removeRestrictedArea(self):
		for i in range(len(self.total_area)):
			point = Point(self.total_area[i])
			if point.within(self.restricted_area):
				self.good[i] = 0

		self.drawShape()

	def singlethreadReduce(self, new_coord):
		self.good = self.reduce(new_coord, self.total_area, self.good)

	def simplethread(self, coord):
		t = threading.Thread(target=self.singlethreadReduce, args=(coord,))
		t.start()


	def reduce(self, new_coord, total_area, good):
		if self._debug:
			thread = self.thread
			print("Start thread: ", thread)

		r = geodesic_point_buffer(new_coord[0], new_coord[1], self.radius)
		r_polygon = Polygon(r)

		for i in range(len(total_area)):
			if good[i]:
				point = Point(total_area[i])
				if not point.within(r_polygon):
					good[i] = 0

		self.active_threads -= 1
		if self._debug:
			print("Stop thread: ", thread)
		return good


	def drawShape(self):
		savetoKML(self.getPoints(), "changing_area")


	def getPoints(self):
		goodpoints = []
		#print(len(self.total_area))
		for i in range(len(self.total_area)):
			if self.good[i]:
				goodpoints.append(self.total_area[i])
		return goodpoints

	def getGoodMask(self):
		return self.good

	def startGISthread(self):
		t = threading.Thread(target=self.integrateGIS)
		t.start()

	def integrateGIS(self):
		fp = open("visualization/coords.txt","w")
		points = self.getPoints()
		for coord in points:
			fp.write("(" + str(coord[0]) + "," + str(coord[1]) + ")\n")
		fp.close()
		os.system("C:/Users/" + getpass.getuser() + "/AppData/Local/Programs/ArcGIS/Pro/bin/Python/Scripts/propy.bat \
			\"C:/summer-games/EFOC/pilot_locator/referenceGIS.py\" visualization/coords.txt")
		process_landclasses(points, "visualization/landclasses.txt")
		self.openHeatmap()

	def openHeatmap(self):
		os.startfile("visualization\\legend2.kml")
		os.startfile("visualization\\liveheatmap.kml")
		#clearKML("changing_area")

	def run(self, coord):

		if self.first_time:
			self.thread += 1
			self.start(coord)
			self.first_time = False
		else:
			if self.active_threads < self.max_threads:
				self.thread += 1
				self.active_threads += 1
				self.simplethread(coord)
			else:
				self.drop_count += 1
				if self._debug:
					print("dropped: ", self.drop_count)

		if self.thread % 4 == 0:
			self.drawShape()