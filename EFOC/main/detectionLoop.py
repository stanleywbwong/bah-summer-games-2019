#imports
import redis
import traceback
import json
import pandas as pd


#function body
def RedisCheck():
	
	r = redis.StrictRedis(host='192.168.10.110', port=6379, charset="utf-8", decode_responses = True) #connects to the server

	p = r.pubsub() #
	p.subscribe('simulation') #subscribes to a specified data stream layer

	for item in p.listen(): #pulls each new message from the server (endless loop)
		try:
			
			message = item['data'] #following bits pull out and convert server data to a readable format
			
			#message = str(message)
			#message = message.strip(" ' ")
			messageDict = json.loads(message)
			
			coordStream = messageDict['data']['centerpoints'][0] #get the coordinates from server data

			#timestamp = messageDict['data']['timestamp'] #gets the timestamp 
			
			coordList = list(coordStream.values()) #converts dict to list 
		
			#yield coordList #returns each new coordinate pair without stoping the function 
			yield coordList
			
		except Exception as e: #the first message from the server is null, this allows the loop to continue
			print(e)



#function call for tests
'''
serverCoords = RedisCheck()	
for result in serverCoords:
	print((result))
'''


def RedisParse(item):
	try:
		message = item['data'] #following bits pull out and convert server data to a readable format
		
		#message = str(message)
		#message = message.strip(" ' ")
		messageDict = json.loads(message)
		
		coordStream = messageDict['data']['centerpoints'][0] #get the coordinates from server data

		#timestamp = messageDict['data']['timestamp'] #gets the timestamp 
		
		coordList = list(coordStream.values()) #converts dict to list 
	
		#yield coordList #returns each new coordinate pair without stoping the function 
		return coordList
		
	except Exception as e: #the first message from the server is null, this allows the loop to continue
		print(e)

