
f = open("config.txt")

drones = [0, 2, 3, 4]
folder = ""
timeout = 5
bind_port = 53486
drone_addr = ['10.42.0.171', '10.42.0.207', '10.42.10.174', '10.42.0.192', '10.42.0.187']
drone_port = [8889, 8889, 8889, 8889, 8889]


if f.mode == "r":
	drones = f.readline().strip("\n").split(' ', 1)[1].split(" ")
	drones = list(map(int, drones))
	print(drones)

	folder = f.readline().strip("\n").split(' ', 1)[1]
	print(folder)
	
	temp = f.readline().strip("\n")
	if temp is not "":
		timeout = int(temp.split(' ', 1)[1])
	print(timeout)
	
	temp = f.readline().strip("\n")
	if temp is not "":
		bind_port = int(temp.split(' ', 1)[1])
	print(bind_port)


	temp = f.readline().strip("\n")
	if temp is not "":
		drone_addr = temp.strip("\n").split(' ', 1)[1].split(" ")
		print(drone_addr)

	temp = f.readline().strip("\n")
	if temp is not "":
		drone_port = temp.strip("\n").split(' ', 1)[1].split(" ")
		drone_port = list(map(int, drone_port))
		print(drone_port)