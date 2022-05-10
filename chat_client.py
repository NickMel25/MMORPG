import socket


class Chat_client:
    def __init__(self, ip : str) -> None:
        # self.ip = socket.gethostbyname(socket.gethostname())
        self.ip = ip
        self.port = 13372
        self.chat_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    

    def close_connection(self) -> None:
        self.chat_client.close()


    def connect(self,username):
        self.chat_client.connect((self.ip,self.port))
        self.chat_client.send(username.encode())

    def send_message(self, msg : str):
        self.chat_client.sendall(msg.encode())
            


    def recv(self):
        data = self.chat_client.recv(1024)
        if not data:
            return None
        return data.decode()
        

