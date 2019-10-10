#Peter Malinovsky
#605277
#Booz Allen Hamilton
#Summer Games 2019


import redis
import time
from track_importer import Track, findFiles


#getString
#Inputs: int timestamp in Unix epoch format, tuple centerpoints of drone, tuple offset of drone
#Return: string formatted as layer4 data for enforcefield server as of 7/12/19
def getString(timestamp, centerpoints, offset):
	return "{\"data\": {\"id\": \"layer4\", \"timestamp\": %d, \"centerpoints\": [{\"x\": %f, \"y\": %f, \"z\": %f}], \"offset\": [{\"x\":%f, \"y\":%f, \"z\":%f}]}}" \
	% (timestamp, centerpoints[0], centerpoints[1], centerpoints[2],  offset[0], offset[1], offset[2])


#simulate
#Inputs: tuple centerpoints of drone, tuple offset of drone, delay before returning
#Return: nothing
def simulate(centerpoints, offset, delay):
	r.publish('simulation', getString(time.time() * 1000, centerpoints, offset))
	time.sleep(delay)


#interpolateSimulator
#Inputs: filename of track file to open ** NOTE: must be track file, not path file, timestamps are need **, delay time interval in between coordinates
#Return: 0 on success, 1 on error
def interpolateSimulator(filename, delta):
	t = Track(filename)
	start_time = 0
	secs = 0
	coord = []

	for elem in range(t.getSize() - 1):

		if start_time == 0:
			secs, coord = t.getNext()
			if secs == 0:
				return 1
			start_time = secs
		
		next_secs, next_coord = t.getNext()

		diff = next_secs - secs
		diff /= delta
		diff = int(diff)

		for i in range(diff):
			temp_secs = interpolate(secs, next_secs, i, diff)
			temp_coord = [interpolate(coord[j], next_coord[j], i, diff) for j in range(len(coord))]

			print(str(temp_secs) + ' : ' + str(temp_coord))

			simulate(temp_coord, [0, 0, 0], delta)

		secs = next_secs
		coord = next_coord

	simulate(coord, [0, 0, 0], 0)
	return 0


#interpolate
#Inputs: maximum value in interpolation, minimum value in interpolation, count index out of total, total iteration count
#Return: interpolated value
def interpolate(minimum, maximum, count, total):
	diff = maximum - minimum
	delta = diff / total
	current = delta * count
	return current + minimum


#openFile
#Inputs: filename to open
#Return: 0 on success, 1 on failure
def openFile(filename):
	t = Track(filename)
	start_time = 0
	secs = 0
	coord = []

	for elem in range(t.getSize() - 1):

		if start_time == 0:
			secs, coord = t.getNext()
			if secs == 0:
				return 1
			start_time = secs
		
		next_secs, next_coord = t.getNext()
		delta = next_secs - secs

		print(str(secs) + ' : ' + str(coord))

		simulate(coord, [0, 0, 0], delta)
		secs = next_secs
		coord = next_coord

	simulate(coord, [0, 0, 0], 0)
	return 0


#infiniteLoop
#Inputs: none
#Return: nothing
def infinteLoop():
	centerpoints = [-71.2743, 42.4580, 50]
	offset = [1, 2, 3]
	delay = .1

	print(getString(123, [1, 2, 3], [1, 2, 3]))

	while True:

		for i in range(100):
			simulate(centerpoints, offset, delay)
			centerpoints[0] += 0.001

		for i in range(100):
			simulate(centerpoints, offset, delay)
			centerpoints[1] += 0.001

		for i in range(100):
			simulate(centerpoints, offset, delay)
			centerpoints[0] -= 0.001

		for i in range(100):
			simulate(centerpoints, offset, delay)
			centerpoints[1] -= 0.001


#Main simulator body, can modify redis parameter if being used with a different network configuration


r = redis.Redis(host = '192.168.10.110', port = 6379, charset="utf-8", decode_responses = True)
p = r.pubsub()

interpoator = True
delta = .1


while True:
	print()
	print("#        : Custom Path")
	print("NO INPUT : Infinte Loop")
	print("99       : Exit\n")
	print("Paths found: ")
	files = findFiles()
	for i in range(len(files)):
		print(str(i) + ' - ' + files[i])

	val = input("Please select a path to simulate: ")
	if val == '':
		infinteLoop()

	val = int(val)
	if val == 99:
		exit()

	f = files[val]
	print(f)
	if interpoator:
		if interpolateSimulator(f, delta):
			print("Error opening track")
	else:
		if openFile(f):
			print("Error opening track")

