"""
Program for running a set of prewritten, line-by-line Tello drone commands in commands.txt

"""

import threading 
import socket
import sys
import time

def sendMessage(msg):
    print(msg)
    msg = msg.encode(encoding="utf-8") 

    sock.settimeout(4)
    r = 3 #number of messages to be sent

    for i in range(0, r + 1):
        sent = sock.sendto(msg, tello_address)
        try:
            data, server = sock.recvfrom(8890)
            print(data.decode(encoding="utf-8"))

            if data.decode(encoding="utf-8") == "error":
                print("Drone not okay")
                exit()
                
            return
        except:
            print("Message", i, "failed")
            if i == r:
                print("Drone not okay")
                exit()

"""
Create a UDP socket

"""
host = ''
port = 9000
locaddr = (host,port)
# local address:
tello_address = ('192.168.10.1', 8889)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(locaddr)


"""
Read in commands

"""
f = open("commands.txt", "r")

if f.mode == 'r':
    line = f.readline()
    line = line.rstrip("\n")
    
    while line:
        sendMessage(line)
        line = f.readline()
        line = line.rstrip("\n")

f.close()
sock.close()  


