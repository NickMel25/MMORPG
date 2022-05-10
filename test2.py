import socket
from time import sleep
from threading import Thread

ip = '0.0.0.0'
port = 12345
# port = 16985
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((ip,port))
not_udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
not_udp_server.bind((ip,45678))

ans,conn = not_udp_server.recvfrom(1024)
print(ans)
not_udp_server.sendto(b's',conn)
def second():
    
    while True:
        ans, conn = udp_server.recvfrom(1024)
        ans = int(ans.decode())+2
        print(ans)
        udp_server.sendto(str(ans).encode(),conn)
        sleep(3)

thread = Thread(target=second)
thread.start()
while True:
    ans, conn = not_udp_server.recvfrom(1024)
    ans = int(ans.decode())+1
    print(ans)
    not_udp_server.sendto(str(ans).encode(),conn)
    sleep(3)
