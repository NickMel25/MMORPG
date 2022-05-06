import encryption
import socket
import threading
from Crypto.PublicKey import RSA
import db_access

class End_conn_serv:
    # END CONNECTION, NEED TO DECIDE HOW TO SAVE ALL CHANGES!!!!!!!!!!!!!!!!
    def __init__(self,client_list,client_data) -> None:
        self.port = 57141
        self.ip = '0.0.0.0'
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_connection.bind((self.ip,self.port))

        self.private_key, self.public_key = encryption.assymetric_generate_keys()
        self.client_list = client_list
        self.client_data = client_data

    def connecting(self):
        self.server_connection.listen()
        conn, addr = self.server_connection.accept()
        return conn, addr


    def thread_handler(self,conn,addr):
        # ans = conn.recv(1024*4)
        # username = [k for k, v in self.client_list.items() if v['conn']['ip'] == addr[0]][0]
        # pad_char = self.client_list[username]['conn']['pad_char']
        # secret_key = self.client_list[username]['conn']['seckey']
        # decrypted_ans = encryption.symmetric_decrypt_message(ans,secret_key,pad_char)
        username = [k for k, v in self.client_list.items() if v['conn']['ip'] == addr[0]][0]
        pad_char = self.client_list[username]['conn']['pad_char']
        secret_key = self.client_list[username]['conn']['seckey']
        
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
        encrypted_result = encryption.symmetric_encrypt_message(result,secret_key,pad_char)
        conn.sendall(encrypted_result)
        
        

def main(client_list,client_data):
    end_conn_serv = End_conn_serv(client_list,client_data)
    while True:
        conn,addr = end_conn_serv.connecting()
        thread = threading.Thread(target=end_conn_serv.thread_handler,args=[conn,addr])
        thread.daemon = True
        thread.start()
        print("created new thread")

if __name__ == "__main__":
    main()