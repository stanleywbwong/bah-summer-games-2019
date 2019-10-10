import simplekml
def visualizeGPSOutput(filename, name, location):
	'''
	This function writes a file containing the gps location of the located drone.
	It is continuously updated for each new location input
	'''
	with open ("visualization/" + filename, "w") as pos:
		pos.write(
"""<kml xmlns="http://www.opengis.net/kml/2.2"
 xmlns:gx="http://www.google.com/kml/ext/2.2">
	<Placemark>
		<name>%s</name>
		<description>Python Output</description>
		<Style id="sh_icon">
			<IconStyle>
				<scale>2</scale>
				<Icon>
					<href>resources\\icon.png</href>
				</Icon>
			</IconStyle>
		</Style>
  		<Point>
  			<altitudeMode>relativeToGround</altitudeMode>
    		<coordinates>%s,%s,%s</coordinates>
  		</Point>
	</Placemark>
</kml>""" % (name, location[0], location[1], location[2]))

	'''
		kml = simplekml.Kml()
	descript = "Drone Model: Tello EDU\n" + "Current Coordinates: (%s, %s, %s)" % (location[0], location[1], location[2])
	pos = kml.newpoint(name = name, description = descript, coords = [(location[0], location[1], location[2])])
	pos.altitudeMode = simplekml.AltitudeMode.relativetoground
	pos.style.iconstyle.icon.href = "icon.png"
	pos.style.iconstyle.scale = 2
	kml.save("visualization\\" + filename)
	'''

def clearPoint(filename, location):
	'''
	This function clears the previous point and replaces it with the new input
	'''
	'''
	with open ("visualization/" + filename, "w") as pos:
		pos.write(
"""<kml xmlns="http://www.opengis.net/kml/2.2"
 xmlns:gx="http://www.google.com/kml/ext/2.2">
	<Placemark>
		<name></name>
		<description>Python Output</description>
		<Style id="sh_icon">
			<IconStyle>
				<scale>2</scale>
				<Icon>
					<href>resources\\blank.png</href>
				</Icon>
			</IconStyle>
		</Style>
  		<Point>
  			<altitudeMode>relativeToGround</altitudeMode>
    		<coordinates>%s,%s,%s</coordinates>
  		</Point>
	</Placemark>
</kml>""" % (location[0], location[1], location[2]))
'''

	kml = simplekml.Kml()
	pos = kml.newpoint(name = "", description = "UAV", coords = [(location[0], location[1], location[2])])
	pos.altitudeMode = simplekml.AltitudeMode.relativetoground
	pos.style.iconstyle.icon.href = None
	#pos.displayMode = simplekml.DisplayMode.hide
	kml.save("visualization\\" + filename)

#function call for tests
'''
import time
filename = "position.kml"
name = "Drone 1"
gps = [42.467749, -71.262165]
for i in range(5):
	visualizeGPSOutput(filename, name, gps)
	time.sleep(1)
	gps[1] -= .001
for i in range(5):
	visualizeGPSOutput(filename, name, gps)
	time.sleep(1)
	gps[1] += .001
clearPoint(filename, gps)
'''