import socket
import threading
import time

ip = '192.168.68.113'

port = 13378
server_address = (ip,port)
chat_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_client.connect(server_address)
username = 'Ben'
text = ''

def send_message(msg):
    global chat_client
    chat_client.sendall(str.encode(msg))
        

def init(user):
    global username
    username = user
    chat_client.sendall(str.encode(username))


def main():
    global chat_client
    data = chat_client.recv(1024)
    print(data)
    if not data:
        return None
    return data.decode()
        

if __name__ == '__main__':
    main(username)