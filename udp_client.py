import socket
from threading import Thread
import client_performer


class Udp_client:
    def __init__(self, ip : str) -> None:

        # self.ip =socket.gethostbyname(socket.gethostname())
        self.server_ip = ip
        self.ip = socket.gethostbyname(socket.gethostname())
        self.player_port = 10001
        self.port = 12345
        self.udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.udp_client.bind((self.ip,self.port))

        self.monster_port = 32456
        self.monster_udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def bind(self,port):
        self.monster_udp_client.bind((socket.gethostname(),port))

    def recv_monster_thread_handler(self):
        while True:
            try:
                monster_data = self.recieve_for_monster()
                answer = monster_data.decode().split(":")
                client_performer.print_monsters_around_player(answer)
            except:
                pass

    def start_monster_thread(self,player, level):
        # arr = {"player" : player,
        #  "level" : level}

        client_performer.get_player(player, level)
        players_nearby_thread = Thread(target=self.recv_monster_thread_handler, daemon=True)
        players_nearby_thread.start()

    def recieve_for_monster(self):
        msg, conn = self.monster_udp_client.recvfrom(1024)
        return msg

    def close_connection(self):
        self.udp_client.close()
        self.monster_udp


    def set_username(self,username):
        self.username = username 

    def recv_thread_handler(self,player,level):
        while True:
            data = self.receive()
            if data:
                data = data
                try:
                    client_performer.display_players(data.decode(),player,level)
                except:
                    pass

    def receive(self):
        try:
            msg ,conn = self.udp_client.recvfrom(1024)
            return msg
        except:
            return False

    def send(self, msg : str):
        self.udp_client.sendto(self.username.encode()+"∞".encode()+msg.encode(),(self.server_ip,self.player_port))


    # def proccess(self,data):    
    #     self.send(data)
    #     ans = self.receive()
    #     print(ans)

    def start_thread(self,player,level):
        players_nearby_thread = Thread(target=self.recv_thread_handler, daemon=True, args=(player,level))
        players_nearby_thread.start()

