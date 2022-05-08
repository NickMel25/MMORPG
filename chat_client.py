import socket
import encryption

class Chat_client:
    def __init__(self, ip : str, secret_key : bytes, private_client_key, public_client_key, public_server_key, pad_char : str) -> None:
        # self.ip = socket.gethostbyname(socket.gethostname())
        self.ip = ip
        self.port = 13372
        self.chat_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.secret_key = secret_key
        self.private_client_key = private_client_key
        self.public_client_key = public_client_key
        self.public_server_key = public_server_key
        self.pad_char = pad_char
    

    def close_connection(self) -> None:
        self.chat_client.close()


    def connect(self):
        self.chat_client.connect((self.ip,self.port))

    def send_message(self, msg : str):
        encrypted_msg = encryption.symmetric_encrypt_message(msg,self.secret_key,self.pad_char)
        self.chat_client.sendall(encrypted_msg)
            


    def recv(self):
        data = self.chat_client.recv(1024)
        if not data:
            return None
        return encryption.symmetric_decrypt_message(data,self.secret_key,self.pad_char)
        
