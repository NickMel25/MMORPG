import socket


server_IP = '10.0.0.185'
server_port = 13372
udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def receive():
        msg = udp_client.recvfrom(1024)
        print(msg)
        return msg

def send(msg):
    global server_IP
    global server_port
    udp_client.sendto(str.encode(msg),(server_IP,server_port))

def main():
    while True:
        msg = input("please insert a msg to the server")
        
        send(msg)

        ans = receive()
        print(ans)

if __name__ == "__main__":
    main()