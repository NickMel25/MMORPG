import socket
import threading
from Crypto.PublicKey import RSA
import db_access

class End_conn_serv:
    
    def __init__(self,client_list) -> None:
        self.port = 57141
        self.ip = '0.0.0.0'
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_connection.bind((self.ip,self.port))
        self.client_list = client_list
    
    
    def close_connection(self):
        self.server_connection.close()


    def connecting(self):
        self.server_connection.listen()
        conn, addr = self.server_connection.accept()
        return conn, addr


    def thread_handler(self,conn,addr):
        username = conn.recv(1024).decode()
        data = []
        data.append(self.client_list[username]['game']['health'])
        data.append(self.client_list[username]['game']['mana'])
        data.append(self.client_list[username]['game']['location'][0])
        data.append(self.client_list[username]['game']['location'][1])
        data.append(self.client_list[username]['game']['attack'])
        data.append(self.client_list[username]['game']['bamboo'])
        data.append(self.client_list[username]['game']['bloodpotion'])
        data.append(self.client_list[username]['game']['spiritinabottle'])
        data.append(self.client_list[username]['game']['coins'])
        result = db_access.update(username,data)
        conn.sendall(result.encode())
        self.client_list.pop(username)
        
        

    def main(self):
        while True:
            conn,addr = self.connecting()
            thread = threading.Thread(target=self.thread_handler,args=[conn,addr])
            thread.daemon = True
            thread.start()
 
