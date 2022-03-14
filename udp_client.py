import socket


server_IP = '192.168.117.198'
server_port = 13372
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def recv_thread_handler():
    data = receive()
    data = data.decode()


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

