import socket
from threading import Thread
from time import sleep 
monster_udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
not_monster_udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
not_monster_udp_client.sendto(b's',('10.0.0.169',45678))
ans = not_monster_udp_client.recvfrom(1024)
print(ans)

def second():
    monster_udp_client.sendto('1'.encode(),('10.0.0.169',12345))
    while True:
        ans, conn = monster_udp_client.recvfrom(1024)
        ans = int(ans.decode())+2
        print(ans)
        monster_udp_client.sendto(str(ans).encode(),conn)
        sleep(3)

thread = Thread(target=second)
thread.start()
not_monster_udp_client.sendto('1'.encode(),('10.0.0.169',45678))
while True:
    ans, conn = not_monster_udp_client.recvfrom(1024)
    ans = int(ans.decode())+1
    print(ans)
    not_monster_udp_client.sendto(str(ans).encode(),conn)
    sleep(3)
