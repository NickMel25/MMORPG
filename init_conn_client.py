from more_itertools import pad_none
import encryption
import socket
from settings import *
from Crypto.PublicKey import RSA

class Init_conn_client:
    
    def __init__(self) -> None:
        self.port = 14175
        self.ip = socket.gethostbyname(socket.gethostname())
        self.client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connection.connect((self.ip,self.port))
        results = self.exchange_keys()
        
        self.secret_key = results[0] 
        self.private_client_key = results[1] 
        self.public_client_key = results[2] 
        self.public_server_key = results[3] 
        self.pad_char = results[4]
    
    
    def close_connection(self) -> None:
        self.client_connection.close()
    
    
    def get_keys(self) -> tuple:
        return self.secret_key,self.private_client_key, self.public_client_key,self.public_server_key,self.pad_char
    

    def exchange_keys(self):
        global secret_key, private_client_key, public_client_key, public_server_key, pad_char

        private_client_key,public_client_key = encryption.assymetric_generate_keys()
        self.client_connection.sendall(public_client_key.publickey().exportKey())

        print("tryting to receive public key")
        public_server_key = self.client_connection.recv(1024*4)
        public_server_key = RSA.importKey(public_server_key, passphrase=None) 

        print("tryting to receive secret key")
        secret_key = self.client_connection.recv(1024*4)
        secret_key = encryption.assymetric_decrypt_message(secret_key,private_client_key)

        print("tryting to receive pad char")
        pad_char = self.client_connection.recv(1024*4)
        pad_char = encryption.assymetric_decrypt_message(pad_char,private_client_key)
        pad_char = pad_char.decode()
        print("all complete")
        
        confirmation_message = 'confriming data recievement'
        encrypted_confirmation_message = encryption.symmetric_encrypt_message(confirmation_message,secret_key,pad_char)
        self.client_connection.sendall(encrypted_confirmation_message)

        return secret_key, private_client_key, public_client_key, public_server_key, pad_char    


    def user_connection(self, mode:str, username :str,password :str,confirmpassword = '') -> list:
        message = f"{mode}:{username}:{password}:{confirmpassword}"
        encrypted_message = encryption.symmetric_encrypt_message(message,self.secret_key,self.pad_char)
        self.client_connection.sendall(encrypted_message)
        encrypted_result = self.client_connection.recv(1024*4)
        result = encryption.symmetric_decrypt_message(encrypted_result,self.secret_key,self.pad_char)
        print(result)
        return result.split(":")

