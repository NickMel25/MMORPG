import socket

ip = '0.0.0.0'
port = 10001
# port = 16985
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((ip,port))

ans , conn = udp_server.recvfrom(1024)
print(ans)
udp_server.send