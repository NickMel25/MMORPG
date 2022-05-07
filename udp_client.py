import socket
import threading

from threading import Thread
import client_performer

server_IP = '10.100.102.10'
ip = socket.gethostbyname(socket.gethostname())
port = 12035
server_port = 16985

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udp_client.bind((ip, port))

monster_udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
monster_udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
monster_udp_client.bind((ip, 54321))


def recv_monster_thread_handler():
    while True:
        try:
            monster_data = recieve_for_monster()
        except Exception as e:
            print(e)

        answer = monster_data.split(":")
        print(answer)
        client_performer.print_monsters_around_player(answer)


def start_monster_thread(player, level):
    # arr = {"player" : player,
    #  "level" : level}
    client_performer.get_player(player, level)
    players_nearby_thread = threading.Thread(target=recv_monster_thread_handler, daemon=True)
    players_nearby_thread.start()


def recieve_for_monster():
    msg, conn = monster_udp_client.recvfrom(1024)
    msg = msg.decode()
    return msg


def recv_thread_handler(player, level):
    while True:
        data = receive()
        data = data
        client_performer.display_players(data, player, level)


def receive():
    msg, conn = udp_client.recvfrom(1024)
    msg = msg.decode()
    return msg


def send(msg):
    global server_IP
    global server_port
    udp_client.sendto(str.encode(msg), (server_IP, server_port))


def proccess(data):
    send(data)
    ans = receive()


def start_thread(player, level):
    # arr = {"player" : player,
    #  "level" : level}
    players_nearby_thread = Thread(target=recv_thread_handler, daemon=True, args=(player, level))
    players_nearby_thread.start()
