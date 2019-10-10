
"""
Test program for converting text files containing 1) geographic lon/lat data of the potential pilot area and 
2) CONUS land classification data encoded as integers into a KML representing a heatmap of pilot location probabilities
Arcpy not required.
"""
from ast import literal_eval
import simplekml

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
	    pntstyle.iconstyle.icon.href = "Solid_white.png"
	    pnt.style = pntstyle
	kml.save("../output/" + name + ".kml")
	print("Pilot location predictions available (see Google Earth)")

if __name__ == '__main__':
	pilot_coords = []
	fp = open("../output/coords.txt", "r")
	lines = fp.readlines()
	for line in lines:
		pilot_coords.append(literal_eval(line.strip('\n')))
	fp.close()

	class_weights = {11: 6, 12: 6, 21: 10, 22: 9, 23: 8, 24: 7, 31: 9, 41: 4, 42: 4, 43: 4, 
					51: 8, 52: 9, 71: 10, 72: 9, 73: 10, 74: 10, 81: 10, 82: 8, 90: 5, 95: 5}
	weight_mask = []
	fp = open("../output/landclasses.txt", "r")
	lines = fp.readlines()
	for line in lines:
		weight_mask.append(class_weights[int(line.strip('\n'))]) #Add weight to weight list by accessing dictionary above


	GIStoKML(pilot_coords, weight_mask, "GIS_Layer")