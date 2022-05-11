from math import floor
from pydoc import cli
import socket
import threading
from  init_conn_serv import Init_conn_serv
from chat_server import Chat_server
from end_conn_serv import End_conn_serv
import atexit
from support import import_csv_layout
import random
import pygame
import copy
# ============================================================================================================================================
# -----------------------------------------------------------------CONSTANTS------------------------------------------------------------------
# ============================================================================================================================================


pygame.init()
clock = pygame.time.Clock()

print(socket.gethostbyname(socket.gethostname()))
ip = '0.0.0.0'
port = 10001
# port = 16985
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((ip,port))

init_conn_serv = None
chat_server = None
end_conn_serv = None

client_time = {'attack':0,'hit':0,"movement":0}
data_list = {'username':'','direction':'','attacking':'','location':'','hitbox':'','frame':'','health':0, 'bamboo':0,'bloodpotion':0,'spiritinabottle':0,'coins':0,'health':0,'mana':0,'attack':0,'weapon':0}
client_conn = {'ip':'',"port":0,"pubkey":'','seckey':'','pad_char':''}
client_data = {'game':copy.deepcopy(data_list),"timers":copy.deepcopy(client_time),'conn':copy.deepcopy(client_conn)}
client_list = {}
enemies_list = []
on_enemies_screen_players = []
moving_monsters = []
monster_count = 50


layouts = {
    'floor': import_csv_layout('map/map_Floor.csv'),
    'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
    'object': import_csv_layout('map/map_Objects.csv'),
    'entities': import_csv_layout('map/map_Entities.csv')
}

ban_list_floor = [274, 273, 271, 252]

tiled_map = []
blabla = {}
for style, layout in layouts.items():
    blabla[style] = layout

monster_data = {
    'squid': {'health': 100, 'exp': 100, 'damage': 20, 'attack_type': 'slash',
              'speed': 3, 'resistance': 3, 'attack_radius': 80,
              'notice_radius': 360, 'location': [], 'attack': False},
    'spirit': {'health': 100, 'exp': 110, 'attack_type': 'thunder',
               'speed': 4, 'resistance': 3, 'attack_radius': 60,
               'notice_radius': 350, 'location': [], 'attack': True},
    'bamboo': {'health': 70, 'exp': 120, 'attack_type': 'leaf_attack',
               'speed': 3, 'resistance': 3, 'attack_radius': 50,
               'notice_radius': 300, 'location': [], 'attack': False}}


# ============================================================================================================================================
# -----------------------------------------------------------------MONSTER--------------------------------------------------------------------
# ============================================================================================================================================


def get_good_placing():
    xEnemy = random.randrange(0, 50)
    yEnemy = random.randrange(0, 56)

    while (int(layouts['floor'][xEnemy][yEnemy])) in ban_list_floor or (int(layouts['boundary'][xEnemy][yEnemy]) != -1) or (int(layouts['object'][xEnemy][yEnemy]) != -1):
        xEnemy = random.randrange(0, 50)
        yEnemy = random.randrange(0, 56)

    return xEnemy, yEnemy


def create_enemies_place():
    global enemies_list
    # arr = [[' ']*56 for i in range(50)]

    for i in range(monster_count):

        info_list = {'type': "", 'health': 0, 'moving': False, 'location': "", 'close_players': "", 'id': 0, 'is_attacking': False, 'should_player_get_damage': False, 'the_player_it_goes_to': '', 'last_attacked': 0, 'should_get_stuff': False}

        xEnemy, yEnemy = get_good_placing()

        type, stats = random.choice(list(monster_data.items()))
        info_list['type'] = type
        info_list['health'] = monster_data[type]['health']
        info_list['location'] = [yEnemy * 64, xEnemy * 64]
        info_list['id'] = i
        enemies_list.append(info_list)


def get_player_monster_distance(player_center, monster_center):
    enemy_vec = pygame.math.Vector2(monster_center)
    player_vec = pygame.math.Vector2(player_center)
    distance = (player_vec - enemy_vec).magnitude()

    if distance > 0:
        direction = (player_vec - enemy_vec).normalize()
    else:
        direction = pygame.math.Vector2()

    return distance, direction


def move_monster(direction, counter):
    global enemies_list
    current_time = pygame.time.get_ticks()

    if (current_time - enemies_list[counter]['last_attacked'])/1000 >= 1:
        speed = monster_data[enemies_list[counter]['type']]['speed']
        direction.x = direction.x * speed
        enemies_list[counter]['location'][0] += int(direction.x)

        direction.y = direction.y * speed
        enemies_list[counter]['location'][1] += int(direction.y)


def get_damage(counter, monster_rect, weapon_rect):
    global enemies_list

    current_time = pygame.time.get_ticks()

    shit = weapon_rect[6:-2]
    arr = shit.split(', ')
    weaponRect = pygame.Rect(int(arr[0]), int(arr[1]), int(arr[2]), int(arr[3]))

    collide = pygame.Rect.colliderect(monster_rect, weaponRect)
    time_passed = (current_time - enemies_list[counter]['last_attacked'])/1000

    if collide and time_passed >= 1:
        enemies_list[counter]['last_attacked'] = pygame.time.get_ticks()
        enemies_list[counter]['health'] -= 50


def check_player_enemy_collision(monster_rect, player_rect, counter, player):
    shit = player_rect[6:-2]
    if shit != '':
        arr = shit.split(', ')
        player_rect = pygame.Rect(int(arr[0]), int(arr[1]), int(arr[2]), int(arr[3]))

        current_time = pygame.time.get_ticks()
        time_passed = (current_time - client_list[player]['game']["last_attacked"])

        collide = pygame.Rect.colliderect(monster_rect, player_rect)

        if collide and time_passed >= 500:
            client_list[player]['game']["last_attacked"] = pygame.time.get_ticks()
            enemies_list[counter]['should_player_get_damage'] = True


def check_death(counter, player):
    global enemies_list

    if enemies_list[counter]['health'] <= 0:

        ans = "get_stuff"

        send_for_monster(ans, (client_list[player]["conn"]['ip'], 32456),client_list[player]["game"]['username'])

        xEnemy, yEnemy = get_good_placing()

        type, stats = random.choice(list(monster_data.items()))

        enemies_list[counter]['health'] = monster_data[type]['health']
        enemies_list[counter]['moving'] = False
        enemies_list[counter]['is_attacking'] = False
        enemies_list[counter]['close_players'] = ""
        enemies_list[counter]['the_player_it_goes_to'] = ""
        enemies_list[counter]['location'] = [yEnemy * 64, xEnemy * 64]


def enemy_player_proximity():
    global enemies_list

    while True:
        counter = 0
        for monster in enemies_list:
            close_players_to_enemy = []
            enemies_list[counter]['the_player_it_goes_to'] = enemies_list[counter]['location']

            for player in client_list:

                check_death(counter, player)

                player_location = (client_list[player]["game"]["location"][0], client_list[player]["game"]["location"][1])
                monster_location = (enemies_list[counter]['location'][0], enemies_list[counter]['location'][1])

                if monster_location[0] - 700 < player_location[0] < monster_location[0] + 700 and monster_location[1] - 400 < player_location[1] < monster_location[1] + 400:
                    on_enemies_screen_players.append(client_list[player])

                distance, direction = get_player_monster_distance(player_location, monster_location)

                if distance <= monster_data[enemies_list[counter]['type']]['notice_radius']:
                    close_players_to_enemy.append(client_list[player])
                    enemies_list[counter]['moving'] = True
                    move_monster(direction, counter)

                weapon_rect = client_list[player]['game']["weapon"]
                monster_rect = pygame.Rect(enemies_list[counter]['location'][0], enemies_list[counter]['location'][1],64, 64)
                check_player_enemy_collision(monster_rect, client_list[player]['game']["hitbox"], counter, player)

                if distance <= monster_data[enemies_list[counter]['type']]['attack_radius'] and client_list[player]['game']["attacking"] == True and client_list[player]['game']["weapon"] != '0' and client_list[player]['game']["hitbox"] != '':

                    enemies_list[counter]['is_attacking'] = True
                    get_damage(counter, monster_rect, weapon_rect)

            enemies_list[counter]['close_players'] = close_players_to_enemy
            counter += 1

        make_monster_string()
        clock.tick(30)


def make_monster_string():
    global enemies_list

    responses_array = []
    counter = 0
    while counter < monster_count:
        response = f"{enemies_list[counter]['type']}:{enemies_list[counter]['health']}:{enemies_list[counter]['moving']}:{enemies_list[counter]['location']}:{enemies_list[counter]['id']}:{enemies_list[counter]['is_attacking']}:{enemies_list[counter]['should_player_get_damage']}:{enemies_list[counter]['the_player_it_goes_to']}"
        enemies_list[counter]['should_player_get_damage'] = False
        responses_array.append(response)
        send_monsters_to_users(responses_array, enemies_list[counter]['close_players'])
        counter += 1


def send_monsters_to_users(responses_array, pipol):
    for response in responses_array:
        for i in range(len(pipol)):
            send_for_monster(response, (pipol[i]["conn"]['ip'], 32456),pipol[i]['game']['username'])


def monster_thread():
    thread_for_monsters_location = threading.Thread(target=enemy_player_proximity, daemon=True, args=())
    thread_for_monsters_location.start()


def send_for_monster(ans, conn,username):
    udp_server.sendto(ans.encode(), (conn[0], conn[1]))


# ============================================================================================================================================
# -----------------------------------------------------------------PLAYER---------------------------------------------------------------------
# ============================================================================================================================================


def proximity(username: str):
    in_proximity = {}

    for cli in client_list:
        if not (cli == username):
            if  client_list[username]['game']['location'][0]-1250 < client_list[cli]['game']["location"][0] <client_list[username]['game']['location'][0]+1250 \
            and client_list[username]['game']['location'][1]-750 < client_list[cli]['game']["location"][1] <client_list[username]['game']['location'][1]+750:
                in_proximity[cli] = client_list[cli]

    return in_proximity


def make_string(username: dict) -> dict:
    # for name in nearby:
        user = client_list[username]
        user_data = f'{user["game"]["username"]}:{user["game"]["direction"]}:{user["game"]["attacking"]}:{user["game"]["location"]}:{user["game"]["hitbox"]}:{user["game"]["frame"]}'
        return user_data


def exists(username: str)-> bool:
    return username in client_list


def append(data: str,conn) -> None:
    global data_list
    
    answers = data.split(":")
    temp_list = data_list
    # client_info = copy.deepcopy(client_data)
    # client_list[answers[0]]= copy.deepcopy(client_data)
    client_info = client_list[answers[0]]
    client_info['game']['username'] = answers[0]
    client_info['game']['direction']= answers[1]
    client_info['game']['attacking'] = bool(answers[2])
    temp = answers[3][1:-1]
    temp =  tuple(map(int, temp.split(',')))
    print(temp)
    client_info['game']['location'] = temp
    client_info['game']['hitbox'] = answers[4]
    client_info['game']['frame'] = int(floor(float(answers[5])))
    client_info['game']['health'] = answers[6]
    client_info['game']['bamboo'] = int(answers[7])
    client_info['game']['bloodpotion'] = int(answers[8])
    client_info['game']['spiritinabottle'] = int(answers[9])
    client_info['game']['coins'] = int(answers[10])
    client_info['game']['weapon'] = answers[11]
    client_info['game']['last_attacked'] = 0
    client_info['conn']['ip'] = conn[0]
    client_info['conn']['port'] = conn[1]


def add_user(username: str) -> None:
    global data_list
    client_list[username]= data_list    


def iterate_users(nearby: dict,user_data) -> None:
    for user in nearby:
        send(user_data,(nearby[user]['conn']['ip'],nearby[user]['conn']['port']))


def send(ans,conn):
    udp_server.sendto(ans.encode(), (conn))


def receive():
    try:
        msg, conn = udp_server.recvfrom(1024)
        username, msg = msg.decode().split("∞")
        if not username in client_list:
            return False
        return msg, conn
    except:
        return False


def main():
    global udp_server, init_conn_serv, end_conn_serv, chat_server, client_list, client_data
    

    
    init_conn_serv = Init_conn_serv(client_list,copy.deepcopy(client_data))
    thread = threading.Thread(target=init_conn_serv.main)
    thread.daemon = True
    thread.start()

    end_conn_serv = End_conn_serv(client_list)
    thread = threading.Thread(target=end_conn_serv.main)
    thread.daemon = True
    thread.start()

    chat_server = Chat_server(client_list)
    thread = threading.Thread(target=chat_server.main)
    thread.daemon = True
    thread.start()
    create_enemies_place()
    monster_thread()
    while True:
        try:
            data,conn = receive()
        except TypeError:
            continue
        if data:
            try:
                append(data,conn)
            except KeyError:
                continue
            nearby = proximity(data.split(":")[0])
            user_data = make_string(data.split(":")[0])
            iterate_users(nearby,user_data)


def close_all():
    global udp_server, init_conn_serv, end_conn_serv, chat_server
    try:
        udp_server.close()
        init_conn_serv.close_connection()
        end_conn_serv.close_connection()
        chat_server.close_connection()
    except:
        pass


if __name__ == "__main__":
    atexit.register(close_all)
    main()
    

