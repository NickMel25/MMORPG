
import socket


# from connection import *
class End_conn_client:
    def __init__(self, ip : str) -> None:
        self.ip = ip
        self.port = 57141

    def end_conn(self,username):
        
        client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_connection.connect((self.ip,self.port))
        client_connection.send(username.encode())
        result = ''
        while result != "Completed successfully":
            result = client_connection.recv(1024*4).decode()

        client_connection.close()
        return result

