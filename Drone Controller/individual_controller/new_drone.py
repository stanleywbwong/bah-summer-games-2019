import socket


tello = ('192.168.10.1', 8889)

drone = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

drone.setsockopt(socket.SOL_SOCKET, 2, 'wlp0s29f7u3')
drone.sendto('command'.encode(), 0, tello)


