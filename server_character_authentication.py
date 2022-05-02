import imp
import socket
from argon2 import PasswordHasher
import mysql.connector
import threading

ip = '0.0.0.0'
port = 13579
conn_list = {}
server_address = (ip,port)
chat_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_server.bind(server_address)

cnn = mysql.connector.connect(user='root',host='localhost',password='4nymbus',database='mmorpg')
crsr = cnn.cursor()

ph = PasswordHasher()



def connecting():
    global chat_server
    chat_server.listen()
    conn, addr = chat_server.accept()
    return conn

def thread_handler(conn):
    pass
    


def main():
    global chat_server
    while True:
        conn = connecting()
        thread = threading.Thread(target=thread_handler,args=[conn])
        thread.daemon = True
        thread.start()
