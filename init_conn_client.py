import encryption
import socket
from settings import *
from Crypto.PublicKey import RSA

class Init_conn_client:
    
    def __init__(self, ip : str) -> None:
        self.port = 14175
        # self.ip = socket.gethostbyname(socket.gethostname())
        self.ip = ip
        self.client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connection.connect((self.ip,self.port))

    
    def close_connection(self) -> None:
        self.client_connection.close()


    def user_connection(self, mode:str, username :str,password :str,confirmpassword = '') -> list:
        message = f"{mode}:{username}:{password}:{confirmpassword}"
        self.client_connection.sendall(message.encode())
        result = self.client_connection.recv(1024*4).decode()
        return result.split(":")


def main():
    init_conn = Init_conn_client()


if __name__ == "__main__":
    main()