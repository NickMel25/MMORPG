from glob import glob
import socket
from datetime import datetime
import threading
from time import sleep

ip = '0.0.0.0'

port = 10234
conn_list = {}
server_address = (ip, port)
chat_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_server.bind(server_address)


def connecting():
    global chat_server
    chat_server.listen()
    conn, addr = chat_server.accept()
    return conn


def thread_handler(conn):
    print("heya")
    global chat_server
    username = conn.recv(1024)
    username = username.decode()
    if not(username in conn_list):
        conn_list[username] = conn
    while True:
        data = conn.recv(1024)

        data = data.decode()
        print(data)
        if not data:
            conn_list.pop(username,None)
            break
        date_now = datetime.now()
        current_time = date_now.strftime("%H:%M")
        ans = f"[{current_time}] {username}: {data}"
        for client in conn_list:
            # if not(username in conn_list):
            conn_list[client].sendall(str.encode(ans))
        sleep(10)


def main():
    global chat_server

    print("connecting")

    while True:
        conn = connecting()
        thread = threading.Thread(target=thread_handler,args=[conn])
        thread.daemon = True
        thread.start()


if __name__ == '__main__':
    main()

