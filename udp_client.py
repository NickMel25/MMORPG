import socket
from threading import Thread
import client_performer

server_IP = '192.168.1.207'
ip =socket.gethostbyname(socket.gethostname())

port = 12345
server_port = 10001

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp_client.bind((ip,port))


def recv_thread_handler(player,level):
    while True:
        data = receive()
        data = data
        print(data)
        client_performer.display_players(data,player,level)


def receive():
        msg ,conn= udp_client.recvfrom(1024)
        msg = msg.decode()
        print(msg)
        return msg


def send(msg):
    global server_IP
    global server_port
    udp_client.sendto(str.encode(msg),(server_IP,server_port))


def proccess(data):    
    send(data)
    ans = receive()
    print(ans)


def start_thread(player,level):
    # arr = {"player" : player,
    #  "level" : level}
    players_nearby_thread = Thread(target=recv_thread_handler, daemon=True, args=(player,level))
    players_nearby_thread.start()

