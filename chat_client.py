import socket
import threading
import time

ip = '10.0.0.169'

port = 13372
server_address = (ip,port)
chat_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_client.connect(server_address)
username = 'Ben'


def input_thread_handler():
    global chat_client
    while True:
        msg = input(f"{username}: ")
        chat_client.sendall(str.encode(msg))
        time.sleep(0.2)


def main():
    global chat_client
    global username
    username = input("enter your username:")
    chat_client.send(str.encode(username))
    thread = threading.Thread(target=input_thread_handler)
    thread.daemon = True
    thread.start()
    while True:
        data = chat_client.recv(1024)
        if not data:
            break
        print(data.decode())
        

if __name__ == '__main__':
    main()