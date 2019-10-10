import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from setup.input_location import setCategory
from setup.Venue import Venue
from main.detectionLoop import RedisParse
from setup.locator_functions import detection
import traceback
from menu_tree.menu_tree import *
from visualization.visualization import visualizeGPSOutput, clearPoint
from setup.shape_viz import *
import os
from os import listdir
from os.path import isfile, join
import redis
from pilot_locator.locator import Operator
from PIL import Image, ImageTk, ImageSequence
import threading
import time

# Class represents window that prompts user to enter level of authorization, airspace category, location, and altitude
class setupGUI():

	# Creates master window
	def __init__(self, master): 
		self.master = master

		w=380; h=280; x=75; y=100

		# Configure size, location, and title of window
		self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
		self.master.title("")
		self.master.configure(background = "#ffffff")

		# Labels and entries

		self.label0 = ttk.Label(self.master, text="EFOC Setup", font = ("Sans Serif", 16), background = "#ffffff")
		self.label0.place(x = 40, y = 0)
		self.line = ttk.Label(self.master, text="                                                                                                                                                                                                                                                                                                                   ",
			font = ("Sans Serif", 2, UNDERLINE), background = "#ffffff")
		self.line.place(x = 32, y = 25)

		self.label1 = ttk.Label(self.master, text="Protocol", font = ("Sans Serif", 12), background = "#ffffff")
		self.label1.place(x = 40, y = 165)

		self.label2 = ttk.Label(self.master, text="Category", font = ("Sans Serif", 12), background = "#ffffff")
		self.label2.place(x = 40, y = 45)

		self.label3 = ttk.Label(self.master, text="Location", font = ("Sans Serif", 12), background = "#ffffff")
		self.label3.place(x = 40, y = 85)

		self.label4 = ttk.Label(self.master, text="Airspace Ceiling (m)", font = ("Sans Serif", 12), background = "#ffffff")
		self.label4.place(x = 40, y = 125)
	                                                                                                                                                                                                                                                                                                                 

		# Read previous configuration text file and set GUI class variables
		self.readConfig()

		# Entry layout
		self.setDropDowns()

		self.e1 = ttk.Entry(self.master, style = "black.TEntry") #Location
		self.e1.insert(END, self.venue)
		self.e1.place(x = 200, y = 85)

		self.e2 = ttk.Entry(self.master, style = "black.TEntry") #Altitude
		self.e2.insert(END, self.alt)
		self.e2.place(x = 200, y = 125)

		# Buttons
		self.runButton = ttk.Button(self.master, text='Run', cursor = "hand2", style = "green.TButton", command = self.openDetection)
		self.runButton.place(x = 265, y = 235)

		# Button Styling		
		self.s = ttk.Style()
		self.s.configure("black.TButton", font = ("Sans Serif", 10), background = "black")
		self.s.configure("black.TEntry", font = ("Sans Serif", 10), background = "black")
		self.s.configure("black.TMenuButton", font = ("Sans Serif", 10), background = "black")
		self.s.configure("green.TButton", font = ("Sans Serif", 11), background = "green", padding = 2)

		ttk.Style().configure("TMenubutton", background = "#98bbf5")
		ttk.Style().configure("TEntry", background = "#98bbf5")
		
		
		self.noError = True


	# Stops any threads running and closes the master window created above
	def close(self):
		try:
			self.thread.stop()
			print("Closed setup GUI")
		except AttributeError as ae:
			print(ae)
		finally:
			self.master.destroy()		

	# Creates drop down menues for location category and level of authorization
	def setDropDowns(self):
		LOCATIONS = [
			"FAA Controlled Airspace",
			"Military Base",
			"National Park",
			"Correctional Facility",
			"Stadium",
			"Power Plant",
			"Foreign Embassy",
		]
		self.getProtocols()

		# Drop down for location category
		self.variable1 = StringVar(self.master)

		self.loc = ttk.OptionMenu(self.master, self.variable1, LOCATIONS[LOCATIONS.index(self.category)], *LOCATIONS)
		self.loc.config(cursor = "hand2")
		self.loc.place(x = 200, y = 45)


		# Drop down for various protocols
		self.variable2 = StringVar(self.master)

		self.prot = ttk.OptionMenu(self.master, self.variable2, self.protocols[self.protocols.index(self.protocol)], *self.protocols)
		self.prot.config(cursor = "hand2")
		self.prot.place(x = 200, y = 165)

	# Reads user's previous configuration from the text file and assigns values to class variables
	def readConfig(self):
		file = open("EFOC_config.txt", "r")
		self.category = (file.readline()).strip()
		self.airspace = setCategory(self.category)
		self.venue = (file.readline()).	rstrip()
		self.alt = (file.readline()).rstrip()
		self.protocol = (file.readline()).rstrip()
		file.close()

	# Checks if user has entered in new inputs and updates class variables if there are new inputs
	def checkNewInput(self):
		if [self.category, self.venue, self.alt, self.protocol] != [self.variable1.get(), self.e1.get(), self.e2.get(), self.variable2.get()]:
			self.category = (self.variable1.get())
			self.airspace = setCategory(self.category)
			self.venue = (self.e1.get()).strip()
			self.alt = self.e2.get().strip()
			self.protocol = (self.variable2.get())
			#print([self.category, self.venue, self.alt, self.protocol])
			return True

	# Creates a list of all profiles in the profiles folder
	def getProtocols(self):
		filelist = []
		for file in os.listdir('roe_profiles'):
			if file.endswith('.profile'):
				filelist.append(file)
		self.protocols = filelist

	# Writes the user inputs to a text file
	def storeInput(self):

		file = open("EFOC_config.txt", "w")
		inputList = [self.category, self.venue, self.alt, self.protocol]
		for i in inputList:
			file.write(i)
			file.write('\n')
		file.close()
		print("Configuration saved")

	# Loads the user's previous configuration by setting the airspace with given class variables
	def loadConfig(self):
		# Checks if user has entered any new input
		if self.checkNewInput():
			# noError is a flag indicating if no errors were raised
			self.noError = True
		# Set up the airspace (raising any errors necessary if user input is invalid)
		try:
			if len(self.venue) == 0:
				raise ValueError('Nothing was entered as location')
			elif isinstance(self.venue, str) == False:
				raise ValueError('Please enter a valid location')
			elif self.category == "FAA Controlled Airspace" and len(self.venue) != 3:
				raise ValueError('Please enter a valid IATA code')
			elif self.category != "FAA Controlled Airspace" and len(self.venue) <= 3:
				raise ValueError('Please enter a valid location name')

			elif (self.airspace.setVenue(self.venue.lower()) == False):
				raise ValueError('Could not find specificed location: ' + self.venue 
									+ "\n" + "Did you mean: " + ', '.join(self.airspace.getPossible()))
			if self.alt.isdigit() == False:
				raise ValueError('Please enter a valid number')
			self.airspace.setAltitude(self.alt)
			self.airspace.setPolygon()
			self.airspace.userConfig[0] = self.category
			self.airspace.userConfig.append(self.protocol)
			
		except ValueError as ve:
			messagebox.showerror("Error", ve)
			self.noError = False
		except AttributeError as ae: 
			messagebox.showerror("Error", "Could not find location name")
			traceback.print_exc()
			self.noError = False
		except Exception:
			messagebox.showerror("Error", "Something went wrong")
			traceback.print_exc()
			self.noError = False
		
	# Opens the detection window by creating an instance of detectGUI class
	def openDetection(self):
		self.loadConfig()
		# If loadConfig did not raise and except any exceptions (meaning airspace setup was successful), then open the detection window
		if self.noError:
			try:
				self.storeInput()
				temp = self.airspace
				detWindow = detectGUI(self.master, self.airspace)
				self.thread = detWindow.getThread()
			except ConnectionError as ce:
				print(ce)
				messagebox.showerror("Error", "Unable to connect to the Redis Server\n Check your connection")
			except AttributeError as err:
				print(err)
				messagebox.showerror("Error", err)

	# Returns a thread
	def getThread(self):
		return self.thread

# Class that represents the detection window			
class detectGUI():

	# Creates the detection window
	def __init__(self, master, airspace):
		self.master = Toplevel(master)
		self.airspace = airspace
		self.master.title("")
		self.count = 0
		self.droneDetected = False
		self.userInformed = False
		self.droneCoords = []


		w=285; h=150; x=75; y=100

		self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))
		self.master.configure(background = "#ffffff")

		# Button Styles
		self.s = ttk.Style()
		self.s.configure("black.TLabel", font = ("Sans Serif", 11), background = "#ffffff")
		self.s.configure("black.TButton", font = ("Sans Serif", 11), background = "black")

		# Creates label
		self.configLabel = ttk.Label(self.master, text = "Looking for drones in \n" + self.airspace.userConfig[1].upper(), style = "black.TLabel", wraplength = 250)
		self.configLabel.place(x = 75, y = 20)

		# Creates button
		self.cancelButton = ttk.Button(self.master, text = "Cancel", style = "black.TButton", command = self.on_closing)
		self.cancelButton.place(x= 100, y = 110)

		# Adds loading gif
		self.canvas = Canvas(self.master, width = 160, height = 30, bd = 0, highlightthickness = 0)
		self.canvas.place(x = 69, y = 65)		
		self.sequence = [ImageTk.PhotoImage(img)
							for img in ImageSequence.Iterator(
									Image.open(r"visualization\\resources\\load.gif"))]
		self.image = self.canvas.create_image(80, 15, image = self.sequence[0])

		self.stopAnimate = False
		self.t = threading.Thread(target=self.animate)
		self.t.start()
		

		# Set up Google Earth visualization and subscribes to Redis server
		#warning = Warning(self.master, self.airspace.userConfig, None)
		try:
			#visualizeGPSOutput("position.kml", "UAV 1", (0, 0, 0))
			self.setupViz()
			self.master.lift()
			self.master.attributes("-topmost", True)
			#self.master.after_idle(self.master.attributes, "-topmost", False)
			r = redis.StrictRedis(host='192.168.10.110', port=6379, charset="utf-8", decode_responses = True)
			p = r.pubsub()
			p.subscribe(**{'simulation': self.detectDrone})
			self.thread = p.run_in_thread(sleep_time=0.001) #Creates separate thread

			self.operator = Operator(.5, 4, 2)

		except Exception as e:
			print(e)
			traceback.print_exc()

	def animate(self):
		while True:
			for counter in range(len(self.sequence)):
				if self.stopAnimate:
					exit()
				self.canvas.itemconfig(self.image, image = self.sequence[counter])
				time.sleep(.02)
				
	# Handles all incoming coordinates from the server and determines if the coordinates are within airspace polygon
	def detectDrone(self, message):
		# Obtains coordinates from Redis server
		result = RedisParse(message)
		coord = (result[1], result[0])
		self.operator.run(coord)

		# Determines if coordinates are within airspace polygon
		status = detection(result, self.airspace.getPolygon(), self.airspace.getShapeData(), self.airspace.getAltitude())
		
		# Updates the KML files with current drone coordinates
		visualizeGPSOutput("position.kml", "UAV 1", result)
		self.droneCoords.append(tuple(result))
		drawPath(self.droneCoords, "path")

		# If drone is detected within the airspace, instance of Warning class created
		if status and not self.userInformed:
			print("Drone is detected")
			self.master.withdraw()
			drawBox("intrusion_info", result)
			os.startfile("visualization\\intrusion_info.kml")
			warning = Warning(self.master, self.airspace.userConfig, self.operator)
			self.userInformed = True
			self.stopAnimate = True

	# Closes detection window
	def on_closing(self):
		try:
			self.stopAnimate = True
			self.thread.stop()
			print("Closed detection GUI")
		except AttributeError as ae:
			print(ae)
		finally:
			self.master.destroy()

	# Opens visualization of airspace, drone position, drone path, and drone pilot locator in Google Earth
	def setupViz(self):
		clearPoint("intrusion_info.kml", (0, 0, 0))
		clearPoint("position.kml", (0, 0, 0))
		clearKML("path") # Clears the previously saved drone path
		os.startfile("visualization\\liveposition.kml")
		os.startfile("visualization\\livepath.kml")
		os.startfile("visualization\\livepilot.kml")
		os.startfile("visualization\\legend1.kml")
		os.startfile("visualization\\intrusion_info.kml")
		os.startfile("visualization\\boundary.kml")
		createBounds(outerBound(format(self.airspace.getPolygon(), self.airspace), self.airspace.getAltitude()), innerBound(format(self.airspace.getPolygon(), self.airspace),0))

	# Retrieves the thread that handles incoming coordinates from the server
	def getThread(self):
		return self.thread

# Class that represents the warning window when a drone is detected inside the forbidden airspace
class Warning():
	#Creates the warning window
	def __init__(self, master, config, operator):
		self.master = Toplevel(master)
		self.master.bell()
		self.master.lift()
		self.master.attributes("-topmost", True)
		self.master.after_idle(self.master.attributes, "-topmost", False)

		self.master.title("")
		self.config = config
		self.operator = operator
		self.master.configure(background = "#ffffff")


		w=540; h=125; x=75; y=100

		self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))

		# Button Styles
		self.s = ttk.Style()
		self.s.configure("black.TButton", font = ("Sans Serif", 10), background = "black")

		# Creates Label
		self.warningLabel = ttk.Label(self.master, text = "Drone detected in " + config[1].upper(), font = ("Sans Serif", 13), wraplength = 350, background = "#ffffff")
		self.warningLabel.place(x = 145, y = 45)

		# Creates Button
		self.okButton = ttk.Button(self.master, text='OK', cursor = "hand2", style = "black.TButton", command=self.openRoE)
		self.okButton.place(x = 435, y =90)

		#Inserts image of warning sign
		path = r"visualization\\resources\\ras.jpg"

		self.img = ImageTk.PhotoImage(Image.open(path))
		panel = tk.Label(self.master, image = self.img, highlightthickness = 0, borderwidth = 0)
		panel.place(x = 50, y = 10)

	# Open the RoE window by creating an instance of the RoE class
	def openRoE(self):
		self.master.withdraw()
		newWindow = RoE(self.master, self.config, self.operator)

# Class that represents the Rules of Engagement module
class RoE():
	#Initializes the RoE window
	def __init__(self, master, airspaceConfig, operator):
		self.root = Toplevel(master)
		self.root.lift()
		self.root.attributes("-topmost", True)
		self.root.after_idle(self.root.attributes, "-topmost", False)
		self.protocol = airspaceConfig[3]
		self.location = airspaceConfig[0]
		self.operator = operator
		self.loadMenu()
		self.root.withdraw()
		self.mainWindow2()

	# Initializes a node object and sets it up with the correct profile based on location
	def loadMenu(self):
		self.rootMenu = Node('', '')
		self.rootMenu.importFromFile('roe_profiles/' + self.protocol)
		self.current = self.rootMenu
		#self.current.print()

	# Handles the actions of the dynamic RoE by navigating to the appropriate node and opening the appropriate window of that node
	def ROEHandler(self, action, index = 0):
		self.window.destroy()
		if action == 0:
			self.current = self.current.getChild(index)
		elif action == 1:
			self.current = self.current.getParent()
		else:
			print("error")

		if self.current.getChildCount() == 0:
			self.mainWindow()
		elif self.current.getChildLabel(0) == "Yes":
			self.mainWindow2()
		elif self.current.getChildCount() == 1:
			self.mainWindow1()
		elif self.current.getChildCount() == 3:
			self.mainWindow3()
		#elif self.current.getChildCount() == 2:
		#	self.mainWindow2()
		else:
			print("error in child count")
			self.mainWindow()

	#mainWindow
	# Creates a node which represents an action profile/instructions		
	def mainWindow(self):
		self.window = Toplevel(self.root)
		self.window.title(self.current.getTitle())

		w=266; h=150; x=75; y=100

		self.window.geometry("%dx%d+%d+%d" % (w, h, x, y))
		self.window.configure(background = "#ffffff")

		self.text = ttk.Label(self.window, text=self.current.getContent(), font=("Sans Serif bold", 14), wraplength = 200, background = "#ffffff")
		self.text.place(x = 45, y = 0)
		self.ba = tk.Button(self.window, text="Back", padx = 4, font = ("Sans Serif", 10), bg = "#C0C0C0", cursor = "hand2",relief = "groove", command=lambda: self.ROEHandler(1))
		self.ba.place(x = 20, y = 110)

	#mainWindow
	# Creates a node which represents an action profile/instructions		
	def mainWindow1(self):
		self.window = Toplevel(self.root)
		self.window.title(self.current.getTitle())

		w=270; h=180; x=75; y=100

		self.window.geometry("%dx%d+%d+%d" % (w, h, x, y))
		self.window.configure(background = "#ffffff")

		self.s = ttk.Style()
		self.s.configure("pb.TButton", padding=10)
		self.s.configure("black.TButton", font = ("Sans Serif", 12), background = "black", padding = 2)
		#self.s.configure("back.TButton", font = ("Sans Serif", 10), background = "black", highlightcolor = "#C0C0C0")

		self.text = ttk.Label(self.window, text=self.current.getContent(), font=("Sans Serif bold", 14), wraplength = 295, background = "#ffffff")
		self.text.place(x = 80, y = 0)
		self.ba = tk.Button(self.window, text="Back", padx = 4, font = ("Sans Serif", 10), bg = "#C0C0C0", cursor = "hand2",relief = "groove", command=lambda: self.ROEHandler(1))
		self.ba.place(x = 20, y = 140)
		if (self.current.getChildLabel(0) == "Locate UAV Pilot"):
			self.locate = ttk.Button(self.window, text=self.current.getChildLabel(0), cursor = "hand2", style = "black.TButton", command = self.operator.startGISthread)
		else:
			self.locate = tk.Button(self.window, text=self.current.getChildLabel(0), padx = 3, pady = 3, font = ("Sans Serif", 13), relief = "groove", cursor = "hand2")
		self.locate.place(x = 65, y = 60)
		
	#mainWindow2
	#Creates a window of a node with two answer choices/buttons
	def mainWindow2(self):
		self.window = Toplevel(self.root)
		self.window.title(self.current.getTitle())


		w=300; h=210; x=75; y=100

		self.window.geometry("%dx%d+%d+%d" % (w, h, x, y))
		self.window.configure(background = "#ffffff")
		
		# Button Styles
		self.s = ttk.Style()
		self.s.configure("pb.TButton", padding=10)
		self.s.configure("green2.TButton", font = ("Sans Serif", 11), background = "green", foreground = "black", padding = 10)
		self.s.configure("red.TButton", font = ("Sans Serif", 11), background = "red", foreground = "black", padding = 10)

		# Creates Buttons
		self.q = ttk.Label(self.window, font = ("Sans Serif", 14), text=self.current.getContent(), background = "#ffffff", wraplength = 230)
		self.q.place(x = 53, y = 15)
		self.yes = ttk.Button(self.window, text=self.current.getChildLabel(0), cursor = "hand2", style = "green2.TButton", command= lambda: self.ROEHandler(0, 0))
		self.yes.place(x = 25, y = 113)
		self.no = ttk.Button(self.window,text=self.current.getChildLabel(1), cursor = "hand2", style = "red.TButton", command= lambda: self.ROEHandler(0, 1))
		self.no.place(x = 160, y = 113)

	def mainWindow3(self):
		self.window = Toplevel(self.root)
		self.window.title(self.current.getTitle())

		w=430; h=220; x=75; y=100

		self.window.geometry("%dx%d+%d+%d" % (w, h, x, y))
		self.window.configure(background = "#ffffff")

		# Button Styles
		self.s = ttk.Style()
		self.s.configure("pb.TButton", padding=10)
		self.s.configure("black.TButton", font = ("Sans Serif", 12), background = "black", padding = 2)

		# Creates Labels
		self.text = ttk.Label(self.window, text=self.current.getContent(), font=("Sans Serif bold", 14), wraplength = 295, background = "#ffffff")
		self.text.place(x = 145, y = 0)

		self.faa = ttk.Label(self.window, text=self.current.getChildLabel(2), font=("Sans Serif", 13), wraplength = 295, background = "#ffffff")
		self.faa.place(x = 105, y = 50)

		# Creates Buttons
		self.ba = tk.Button(self.window, text="Back", padx = 4, font = ("Sans Serif", 10), bg = "#C0C0C0", cursor = "hand2",relief = "groove", command=lambda: self.ROEHandler(1))
		self.ba.place(x = 20, y = 175)
		if (self.current.getChildLabel(0) == "Locate UAV Pilot"):
			self.locate = ttk.Button(self.window, text=self.current.getChildLabel(0), cursor = "hand2", style = "black.TButton", command = self.operator.startGISthread)
		else:
			self.locate = tk.Button(self.window, text=self.current.getChildLabel(0), padx = 3, pady = 3, font = ("Sans Serif", 13), relief = "groove", cursor = "hand2")
		self.locate.place(x = 30, y = 90)

		self.activate = tk.Button(self.window, text=self.current.getChildLabel(1), bg = "#ffffff", padx = 3, pady = 3, font = ("Sans Serif", 13), relief = "groove", cursor = "hand2")
		self.activate.place(x = 215, y = 90)

	# Closes RoE window
	def closeRoE(self): 
		try:
			print("RoE Closed")
		except AttributeError as ae:
			print(ae)
		finally:
			self.root.destroy()


#==================================
if __name__ == '__main__':
	root = Tk()
	gui = setupGUI(root)

	# Function that closes the GUI and stops any threads that are running
	def on_closing():
		try:
			gui.getThread().stop()
			print("Closed setup GUI")
		except AttributeError as ae:
			print(ae)
		finally:
			root.quit()

	root.protocol("WM_DELETE_WINDOW", on_closing) # Handles the event when the X button is pressed
	root.mainloop()