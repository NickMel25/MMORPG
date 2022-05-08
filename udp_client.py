import socket
from threading import Thread
import client_performer
import encryption




class Udp_client:
    def __init__(self, ip : str, secret_key : bytes, private_client_key, public_client_key, public_server_key, pad_char : str ) -> None:

        # self.ip =socket.gethostbyname(socket.gethostname())
        self.ip = ip
        self.port = 10001
        self.udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_client.connect((self.ip,self.port))

        self.secret_key = secret_key
        self.private_client_key = private_client_key
        self.public_client_key = public_client_key
        self.public_server_key = public_server_key
        self.pad_char = pad_char

    
    def close_connection(self):
        self.udp_client.close()


    def recv_thread_handler(self,player,level):
        while True:
            data = self.receive()
            data = data
            print(data)
            client_performer.display_players(data,player,level)


    def receive(self):
            msg ,conn = self.udp_client.recvfrom(1024)
            decrypted_msg = encryption.symmetric_decrypt_message(msg,self.secret_key,self.pad_char)
            return decrypted_msg

    def send(self, msg : str):
        encrypted_msg = encryption.symmetric_encrypt_message(msg,self.secret_key,self.pad_char)
        self.udp_client.sendto(encrypted_msg,(self.ip,self.port))


    # def proccess(self,data):    
    #     self.send(data)
    #     ans = self.receive()
    #     print(ans)

    def start_thread(self,player,level):
        players_nearby_thread = Thread(target=self.recv_thread_handler, daemon=True, args=(player,level))
        players_nearby_thread.start()

