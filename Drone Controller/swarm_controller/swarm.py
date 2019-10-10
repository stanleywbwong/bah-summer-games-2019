#Peter Malinovsky
#605277
#Booz Allen Hamilton
#Summer Games 2019


import socket
import select
import time

#sendMessage
#Inputs: string of message to send, drone port to send from, drone to send it to, name of drone
#Return: nothing
#Does: sends message to respective drone
def sendMessage(msg, drone, send, name):

	print(str(time.time()) + " : " + name + msg)
	msg = msg.encode()
	drone.sendto(msg, send)


#closeDrone
#Inputs: drone port that server binded to, list of open files, index of drone to close
#Return: nothing
#Does: closes command files and server binded port when all files are closed
def closeDrone(drones, files, index):

	print("Closing drone " + str(index))
	files[index].close()

	for f in files:
		if not f.closed:
			return

	drones[0].close()
	drones.remove(drones[0])


#nextCommand
#Inputs: list of files, drone port to send from, list of drones, index of drone to send to, name of drone, list of waiting drones
#Return: nothing
#Does: acts on next command in file
#NOTE: expansion of lanaguage available here
def nextCommand(files, drones, send, index, name, waiting):

	if files[index].closed:
		return

	line = files[index].readline()
	
	if line == "":
		closeDrone(drones, files, index)
	else:
		line = line.rstrip("\n")

		if isTello(line):
			sendMessage(line.split(' ', 1)[1], drones[0], send[index], name)
			waiting[index] = None
		else:
			wait = (int(line.split(' ')[3]), int(line.split(' ')[5]))
			waiting[index] = wait


#isTello
#Inputs: string of command text
#Return: boolean if command is in Tello SDK or swarm extension
#NOTE: expansion of lanaguage available here
def isTello(line):

	nonTello = ["wait"]

	for keyword in nonTello:
		if line.split(' ', 1)[0] == keyword:
			return False
	return True


#checkWating
#Inputs: list of files, drone port server bind, list of drones to send to, index of drone, name of drone, list of waiting drones, list of instruction each drone is on
#Return: nothing
#Does: checks if any drones are done waiting and has them execute the next command
def checkWaiting(files, drones, send, index, name, waiting, instruction):
	for i in range(len(waiting)):
		if waiting[i] is not None:
			if instruction[waiting[i][0]] >= waiting[i][1]:
				nextCommand(files, drones, send, i, "Drone" + str(i) + ": ", waiting)
				checkWaiting(files, drones, send, i, name, waiting, instruction)


#runDrones
#Input: list of server bind ports, list of drone addresses and ports, folder to pull instructions from
#Return: nothing
#Does: main loop, listens and responds to list of drones
def runDrones(drones, send, folder):
	
	#open command files and create empty responses
	files = []
	response = []
	waiting = [None] * len(send)
	instruction = [0] * len(send)

	for i in range(len(send)):
		filename = folder + "\\drone" + str(i) + ".txt"
		files.append(open(filename, "r"))
		response.append("")

	#send drones first message
	for f in range(len(files)):
		nextCommand(files, drones, send, f, "Drone" + str(f) + ": ", waiting)

	#loop through command communcation with drones
	while drones:

		active_drones, a, b = select.select(drones, [], [], timeout)

		if active_drones == []:	
			print("Timeout")

		for a_d in active_drones:
			data, server = a_d.recvfrom(64)
			index = send.index(server)
			response[index] = data
			name = "Drone" + str(index) + ": "

			print(str(time.time()) + " : " + name + data.decode(encoding="utf-8"))

			if data.decode() == "error":
				print("Drone error")
				closeDrone(drones, files, index)
				break

			instruction[index] += 1

			nextCommand(files, drones, send, index, name, waiting)
			checkWaiting(files, drones, send, index, name, waiting, instruction)




f = open("config.txt")

#Default values
drones = [0, 2, 3, 4]
folder = "4_drone_square_full_sync"
timeout = 5
bind_port = 53486
drone_addr = ['192.168.10.10', '192.168.10.11', '192.168.10.12', '192.168.10.13', '192.168.10.14']
drone_port = [8889, 8889, 8889, 8889, 8889]


send = []
recv = []


if f.mode == "r":
	
	temp = f.readline().strip("\n")
	if temp is not "":
		drones = temp.split(' ', 1)[1].split(" ")
		drones = list(map(int, drones))

	temp = f.readline().strip("\n")
	if temp is not "":
		folder = temp.split(' ', 1)[1]
	
	temp = f.readline().strip("\n")
	if temp is not "":
		timeout = int(temp.split(' ', 1)[1])
	
	temp = f.readline().strip("\n")
	if temp is not "":
		bind_port = int(temp.split(' ', 1)[1])

	temp = f.readline().strip("\n")
	if temp is not "":
		drone_addr = temp.strip("\n").split(' ', 1)[1].split(" ")

	temp = f.readline().strip("\n")
	if temp is not "":
		drone_port = temp.strip("\n").split(' ', 1)[1].split(" ")
		drone_port = list(map(int, drone_port))



recv0 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv0.bind(('', bind_port))
recv.append(recv0)

for i in drones:
	temp = (drone_addr[i], drone_port[i])
	send.append(temp)


runDrones(recv, send, folder)
