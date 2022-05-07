from math import floor
from support import import_csv_layout
import socket
import random
import pygame
import threading

# ============================================================================================================================================
# -----------------------------------------------------------------CONSTANTS--------------------------------------------------------------------
# ============================================================================================================================================

pygame.init()
clock = pygame.time.Clock()


ip = '0.0.0.0'
port = 16985
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((ip, port))
client_dict = {}
client_time = {}
print(ip)

enemies_list = []
on_enemies_screen_players = []
moving_monsters = []
monster_count = 10
last_attacked = 0

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

        info_list = {'type': "", 'health': 0, 'moving': False, 'location': "", 'close_players': "", 'id': 0, 'is_attacking': False, 'should_player_get_damage': False, 'the_player_it_goes_to': ''}

        xEnemy, yEnemy = get_good_placing()

        # arr[xEnemy][yEnemy] = 'x'

        type, stats = random.choice(list(monster_data.items()))
        info_list['type'] = type
        info_list['health'] = monster_data[type]['health']
        info_list['location'] = [yEnemy * 64, xEnemy * 64]
        info_list['id'] = i
        enemies_list.append(info_list)

    # for row in arr:
    #     print(row)
    # pass


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

    speed = monster_data[enemies_list[counter]['type']]['speed']
    direction.x = direction.x * speed
    enemies_list[counter]['location'][0] += int(direction.x)

    direction.y = direction.y * speed
    enemies_list[counter]['location'][1] += int(direction.y)


def get_damage(counter, monster_rect, weapon_rect):
    global enemies_list
    global last_attacked
    current_time = pygame.time.get_ticks()

    shit = weapon_rect[6:-2]
    arr = shit.split(', ')
    weaponRect = pygame.Rect(int(arr[0]), int(arr[1]), int(arr[2]), int(arr[3]))

    collide = pygame.Rect.colliderect(monster_rect, weaponRect)
    time_passed = (current_time - last_attacked)/1000

    if collide and time_passed >= 1:
        last_attacked = pygame.time.get_ticks()
        enemies_list[counter]['health'] -= 10


def check_player_enemy_collision(monster_rect, player_rect, counter):
    shit = player_rect[6:-2]
    arr = shit.split(', ')
    player_rect = pygame.Rect(int(arr[0]), int(arr[1]), int(arr[2]), int(arr[3]))

    collide = pygame.Rect.colliderect(monster_rect, player_rect)
    if collide:
        enemies_list[counter]['should_player_get_damage'] = True


def erase_attacks():
    global enemies_list

    counter = 0
    for monster in enemies_list:
        enemies_list[counter]['should_player_get_damage'] = False


def check_death(counter):
    global enemies_list

    if enemies_list[counter]['health'] <= 0:

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
            closest_player = ["", 1000000000]
            close_players_to_enemy = []

            for player in client_dict:

                check_death(counter)

                player_location = (client_dict[player]["location"][0], client_dict[player]["location"][1])
                monster_location = (enemies_list[counter]['location'][0], enemies_list[counter]['location'][1])

                if monster_location[0] - 700 < player_location[0] < monster_location[0] + 700 and monster_location[1] - 400 < player_location[1] < monster_location[1] + 400:
                    on_enemies_screen_players.append(client_dict[player])

                distance, direction = get_player_monster_distance(player_location, monster_location)

                # if closest_player[1] > distance:
                #     closest_player[0] = client_dict[player]["username"]
                #     closest_player[1] = client_dict[player]["location"]

                if distance <= monster_data[enemies_list[counter]['type']]['notice_radius']:
                    close_players_to_enemy.append(client_dict[player])
                    enemies_list[counter]['moving'] = True
                    # move_monster(direction, counter)
                    enemies_list[counter]['the_player_it_goes_to'] = client_dict[player]["location"]
                else:
                    enemies_list[counter]['the_player_it_goes_to'] = enemies_list[counter]['location']

                if distance is None:
                    continue

                weapon_rect = client_dict[player]["weapon"]
                monster_rect = pygame.Rect(enemies_list[counter]['location'][0], enemies_list[counter]['location'][1],64, 64)
                check_player_enemy_collision(monster_rect, client_dict[player]["hitbox"], counter)

                if distance <= monster_data[enemies_list[counter]['type']]['attack_radius'] and client_dict[player]["attacking"] == 'True':
                    print("attacking me!!!!")
                    enemies_list[counter]['is_attacking'] = True
                    get_damage(counter, monster_rect, weapon_rect)

            # if closest_player_now == enemies_list[counter]['the_player_it_goes_to']:
            #     close_players_to_enemy.remove(client_dict[counter])

            enemies_list[counter]['close_players'] = close_players_to_enemy
            counter += 1

        make_monster_string()
        clock.tick(30)

        erase_attacks()


def make_monster_string():
    global enemies_list

    responses_array = []
    counter = 0
    while counter < monster_count:
        response = f"{enemies_list[counter]['type']}:{enemies_list[counter]['health']}:{enemies_list[counter]['moving']}:{enemies_list[counter]['location']}:{enemies_list[counter]['id']}:{enemies_list[counter]['is_attacking']}:{enemies_list[counter]['should_player_get_damage']}:{enemies_list[counter]['the_player_it_goes_to']}"
        responses_array.append(response)
        send_monsters_to_users(responses_array, enemies_list[counter]['close_players'])
        counter += 1


def send_monsters_to_users(responses_array, pipol):
    for response in responses_array:
        for i in range(len(pipol)):
            send_for_monster(response, (pipol[i]["connection"][0], 54321))


def monster_thread():
    thread_for_monsters_location = threading.Thread(target=enemy_player_proximity, daemon=True, args=())
    thread_for_monsters_location.start()


def send_for_monster(ans, conn):
    udp_server.sendto(str.encode(ans), (conn[0], conn[1]))


# ============================================================================================================================================
# -----------------------------------------------------------------PLAYER---------------------------------------------------------------------
# ============================================================================================================================================


def proximity(username):
    in_proximity = {}
    print(client_dict[username]["location"])
    for cli in client_dict:
        if not (cli == username):
            if client_dict[username]["location"][0] - 1250 < client_dict[cli]["location"][0] < \
                    client_dict[username]["location"][0] + 1250 \
                    and client_dict[username]["location"][1] - 750 < client_dict[cli]["location"][1] < \
                    client_dict[username]["location"][1] + 750:
                in_proximity[cli] = client_dict[cli]
                print("in proximity")
    return in_proximity


def make_string(nearby):
    for name in nearby:
        user = nearby[name]
        nearby[
            name] = f'{user["username"]}:{user["direction"]}:{user["attacking"]}:{user["location"]}:{user["hitbox"]}:{user["frame"]}'
    return nearby


def exists(username):
    return username in client_dict


def append(data):
    temp = ''
    answers = data[0].decode().split(":")
    info_list = {}
    client_dict[answers[0]] = info_list
    info_list["username"] = answers[0]
    info_list["direction"] = answers[1]
    info_list["attacking"] = answers[2]
    temp = answers[3][1:-1]
    temp = tuple(map(int, temp.split(',')))
    info_list["location"] = temp
    info_list["hitbox"] = answers[4]
    info_list["frame"] = int(floor(float(answers[5])))
    info_list["weapon"] = answers[6]
    info_list["connection"] = data[1]
    print(answers)


def iterate_users(nearby, conn):
    for user in nearby:
        send(nearby[user], conn)


def send(ans, conn):
    udp_server.sendto(str.encode(ans), (conn[1][0], conn[1][1]))


def receive():
    msg = udp_server.recvfrom(1024)
    return msg


def main():
    create_enemies_place()
    monster_thread()
    while True:
        data = receive()
        append(data)

        nearby = proximity(data[0].decode().split(":")[0])
        nearby = make_string(nearby)
        iterate_users(nearby, data)


if __name__ == "__main__":
    main()
