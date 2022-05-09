import socket
from threading import Thread
import client_performer
import encryption




class Udp_client:
    def __init__(self, ip : str, secret_key : bytes, private_client_key, public_client_key, public_server_key, pad_char : str ) -> None:

        # self.ip =socket.gethostbyname(socket.gethostname())
        self.server_ip = ip
        self.ip = socket.gethostbyname(socket.gethostname())
        self.player_port = 10001
        self.port = 12345
        self.udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_client.bind((self.ip,self.port))

        self.monster_port = 32456
        self.monster_udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.monster_udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.monster_udp_client.bind((self.ip, self.monster_port))

        self.secret_key = secret_key
        self.private_client_key = private_client_key
        self.public_client_key = public_client_key
        self.public_server_key = public_server_key
        self.pad_char = pad_char
        self.username = ''


    def recv_monster_thread_handler(self):
        while True:
            monster_data = self.recieve_for_monster()
            if (monster_data == "get_stuff"):
                client_performer.get_the_stuff()
            else:
                answer = monster_data.split(":")
                print(answer)
                client_performer.print_monsters_around_player(answer)
    
    def start_monster_thread(self,player, level):
        # arr = {"player" : player,
        #  "level" : level}
        client_performer.get_player(player, level)
        players_nearby_thread = self.threading.Thread(target=self.recv_monster_thread_handler, daemon=True)
        players_nearby_thread.start()


    def recieve_for_monster(self):
        msg, conn = self.monster_udp_client.recvfrom(1024)
        msg = msg.decode()
        return msg







    def close_connection(self):
        self.udp_client.close()
        self.monster_udp


    def set_username(self,username):
        self.username = username 

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
        self.udp_client.sendto(self.username.encode()+" ".encode()+encrypted_msg,(self.server_ip,self.player_port))


    # def proccess(self,data):    
    #     self.send(data)
    #     ans = self.receive()
    #     print(ans)

    def start_thread(self,player,level):
        players_nearby_thread = Thread(target=self.recv_thread_handler, daemon=True, args=(player,level))
        players_nearby_thread.start()

