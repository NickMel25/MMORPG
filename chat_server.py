import socket
from datetime import datetime
import threading
from time import sleep
import encryption
class Chat_server:
    def __init__(self,client_list) -> None:        
        self.ip = '0.0.0.0'
        self.port = 13372
        self.chat_connection_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_connection_server.bind((self.ip,self.port))

        self.client_list = client_list
        self.conn_list = {}


    def close_connection(self):
        self.chat_connection_server.close()

        
    def connecting(self):
        global chat_server
        self.chat_connection_server.listen()
        conn, addr = self.chat_connection_server.accept()
        return conn, addr

    def thread_handler(self,conn,addr):

        username = conn.recv(1024).decode()
        if not(username in self.conn_list):
            self.conn_list[username] = conn
        
        while True:
            data = conn.recv(1024)
            if not data:
                self.conn_list.pop(username,None)
                break
            decrypted_msg = encryption.symmetric_decrypt_message(data, self.client_list[username]['conn']['seckey'], self.client_list[username]['conn']['pad_char'])
            date_now = datetime.now()
            current_time = date_now.strftime("%H:%M")
            ans = f"[{current_time}] {username}: {decrypted_msg}"
            encrypted_ans = encryption.symmetric_encrypt_message(ans, self.client_list[username]['conn']['seckey'], self.client_list[username]['conn']['pad_char'])
            for client in self.conn_list:
                # if not(username in self.conn_list):
                self.conn_list[client].sendall(encrypted_ans)
            sleep(10)



    def main(self):
        while True:
            conn,addr = self.connecting()
            thread = threading.Thread(target=self.thread_handler,args=[conn,addr])
            thread.daemon = True
            thread.start()
    

