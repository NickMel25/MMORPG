import socket

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.recv(1024)