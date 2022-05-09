import encryption
import socket


# from connection import *
class End_conn_client:
    def __init__(self, ip : str, secret_key : bytes, private_client_key, public_client_key, public_server_key, pad_char : str ) -> None:
        self.ip = ip
        self.port = 57141
        self.secret_key = secret_key
        self.private_client_key = private_client_key
        self.public_client_key = public_client_key
        self.public_server_key = public_server_key
        self.pad_char = pad_char
    
    def end_conn(self,username):
        
        client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_connection.connect((self.ip,self.port))
        client_connection.send(username.encode())
        result = ''
        while result != "Completed successfully":
            result = client_connection.recv(1024*4)
            result = encryption.symmetric_decrypt_message(result,self.secret_key,self.pad_char)

        client_connection.close()
        return result

