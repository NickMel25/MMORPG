import socket
from threading import Thread

server_IP = socket.gethostbyname(socket.gethostname())
port = 12345
server_port = 13372
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp_client.bind((server_IP,port))


def recv_thread_handler():
    while True:
        data = receive()
        print("lol")


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

def start_thread():
        players_nearby_thread = Thread(target=recv_thread_handler, daemon=True)
        players_nearby_thread.start()