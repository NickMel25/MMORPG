import socket


ip = socket.gethostbyname(socket.gethostname())
port = 13372
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((ip,port))
print(ip)

def receive():
        msg = udp_server.recvfrom(1024)
        print(msg)
        return msg

def send(msg,ans):
    udp_server.sendto(str.encode(ans), (msg[1][0],msg[1][1]))

def main():
    while True:
        msg = receive()
        ans = f"your message was {msg[0]}"
        send(msg, ans)
if __name__ == "__main__":
    main()
    