from ipaddress import v4_int_to_packed
from random import randrange

from pygame import init
import encryption
import socket
import threading
# import udp_server
from Crypto.PublicKey import RSA
import db_access
 
class Init_conn_serv:

    def __init__(self,sclient_list,sclient_data) -> None:
        self.port = 14175
        self.ip = '0.0.0.0'
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_connection.bind((self.ip,self.port))

        self.private_key, self.public_key = encryption.assymetric_generate_keys()
        self.client_list = sclient_list
        self.client_data = sclient_data
    
    
    def close_connection(self):
        self.server_connection.close()


    def connecting(self):
        self.server_connection.listen()
        conn, addr = self.server_connection.accept()
        return conn, addr


    def thread_handler(self,conn,addr) -> None:
        try:
            # keys exchange and setup
            # conn.sendall(str.encode('blablabla'))

            self.client_public_key = RSA.importKey(conn.recv(1024*4), passphrase=None) 
            conn.sendall(self.public_key.publickey().exportKey())
            secret_key = encryption.symmetric_generate_key()
            encrypted_secret_key = encryption.assymetric_encrypt_message(secret_key,self.client_public_key)
            conn.sendall(encrypted_secret_key)
            pad_char = chr(randrange(1,26)+96)
            encrypted_pad_char = encryption.assymetric_encrypt_message(pad_char.encode(),self.client_public_key)
            conn.sendall(encrypted_pad_char)

            confirmation_message = conn.recv(1024*4)
            confirmation_message = encryption.symmetric_decrypt_message(confirmation_message,secret_key,pad_char)
            # login / signup validity
            redo = True
            while redo:
                encrypted_answer = conn.recv(1024*4)
                decrypted_answer = encryption.symmetric_decrypt_message(encrypted_answer,secret_key,pad_char)
                mode,username,password,confirmpassword = decrypted_answer.split(":")
                if mode == 'login':
                    result = db_access.login(username,password)
                if mode == 'signup':
                    result = db_access.signup(username,password,confirmpassword)

                if result == 'Signup completed' or result == 'Correct password':
                    user_data = db_access.load(username)
                    answer = result+":"+':'.join([str(value) for value in user_data])
                    redo = False
                elif mode == 'login' and (result == 'Incorrect password' or result == 'User not found' or result == 'Name too long'):
                    answer = 'Incorrect username or password:'
                elif mode == 'signup' and (result == 'Username or Password cant be empty' or result == 'Password mismatch' or result == 'Invalid characters' or result == 'Username too long' or result == 'Username taken') :
                    answer = result+":"
                
                encrypted_result = encryption.symmetric_encrypt_message(answer,secret_key,pad_char)
                conn.sendall(encrypted_result)

            username = user_data[0]

            self.client_list[username] = self.client_data.copy()
            self.client_list[username]['game']['username'] = username
            self.client_list[username]['conn']['seckey'] = secret_key 
            self.client_list[username]['conn']['ip'] = addr[0]
            self.client_list[username]['conn']['port'] = addr[1]
            self.client_list[username]['conn']['pad_char'] = pad_char
            self.client_list[username]['conn']['pubkey'] = self.client_public_key
            self.client_list[username]['game']['health'] = user_data[1]
            self.client_list[username]['game']['mana'] = user_data[2]
            self.client_list[username]['game']['location'] = (user_data[3],user_data[4])
            self.client_list[username]['game']['attack'] = user_data[5]
            self.client_list[username]['game']['bamboo'] = user_data[7]
            self.client_list[username]['game']['bloodpotion'] = user_data[8]
            self.client_list[username]['game']['spiritinabottle'] = user_data[9]
            self.client_list[username]['game']['coins'] = user_data[10]
            conn.close()
        except ValueError as e:

            conn.close()
            return
        except ConnectionResetError as e:
            conn.close()
            return
        


    def main(self) -> None:
        while True:
            conn,addr = self.connecting()
            thread = threading.Thread(target=self.thread_handler,args=[conn,addr])
            thread.daemon = True
            thread.start()


def mains():
    init_conn = Init_conn_serv({},{})
    init_conn.main()

if __name__ == "__main__":
    mains()