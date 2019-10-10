#Peter Malinovsky
#605277
#Booz Allen Hamilton
#Summer Games 2019


import os, datetime, time
import xml.etree.ElementTree as ET

#findFiles
#Inputs: none
#Return: list of files that end in kml
def findFiles():
	filelist = []
	for file in os.listdir('tracks'):
		if file.endswith('.kml'):
			filelist.append(file)
	return filelist


#Track class that holds the data of an imported google earth track in a queue like structure
class Track:
	def __init__(self, file):
		self.time = []
		self.coord = []
		self.tree = ET.parse('tracks\\' + file)
		self.index = 0
		self.size = 0
		self.parseKML()

	#print
	#Inputs: none
	#Does: prints the current time and coordinate value the simulation is on
	#Return: nothing
	def print(self):
		for i in range(len(self.time)):
			print(str(self.time[i]) + ' : ' + str(self.coord[i]))

	#parseKML
	#Inputs: none
	#Does: parse KML data from file after reading
	#Return: nothing
	def parseKML(self):
		root = self.tree.getroot()

		folder = root.find('{http://www.opengis.net/kml/2.2}Folder')
		if folder == None:
			return 0, [0, 0, 0]
		placemark = folder.find('{http://www.opengis.net/kml/2.2}Placemark')
		track = placemark.find('{http://www.google.com/kml/ext/2.2}Track')

		for elem in track:
			tag = elem.tag.split("}", 1)[-1].split()[0]

			if tag == 'when':
				t = datetime.datetime.strptime(elem.text, "%Y-%m-%dT%H:%M:%SZ").timetuple()
				self.time.append(float(time.mktime(t)))
				self.size += 1
			if tag == 'coord':
				c = elem.text
				n = c.split()
				f = [float(i) for i in n]
				self.coord.append(f)

	#getNext
	#Inputs: none
	#Return: next time and coordinate value in the data queue
	def getNext(self):
		t = self.time[self.index]
		c = self.coord[self.index]
		self.index += 1
		return t, c

	#getSize
	#Inputs: none
	#Return: size of data queue
	def getSize(self):
		return self.size