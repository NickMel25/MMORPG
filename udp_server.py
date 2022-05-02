from math import floor
import socket
import threading
import chat_server

ip = '0.0.0.0'
port = 10001
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((ip,port))

client_time = {'attack':0,'hit':0,"movement":0}
data_list = {'username':'','direction':'','attacking':'','location':'','hitbox':'','frame':'','bamboo':0,'bloodpotion':0,'spiritinabottle':0,'coins':0,'health':0,'mana':0,'attack':0}
client_conn = {'ip':'',"port":0,"pubkey":'','seckey':''}
client_data = {'game':data_list.copy(),"timers":client_time.copy(),'conn':client_conn.copy()}
client_list = {}

def get_client_list() -> dict:
    return client_list,client_data.copy()

# def proximity(username):
#     in_proximity = {}
#     print(client_list[username]["location"])
#     for cli in client_list:
#         if not (cli == username):
#             if  client_list[username]["location"][0]-1250 < client_list[cli]["location"][0] <client_list[username]["location"][0]+1250 \
#             and client_list[username]["location"][1]-750 < client_list[cli]["location"][1] <client_list[username]["location"][1]+750:
         
#                 in_proximity[cli] = client_list[cli]
#                 print("in proximity")
#     return in_proximity

def proximity(username: str):
    in_proximity = {}
    print(client_list[username]['game']["location"])
    for cli in client_list:
        if not (cli == username):
            if  client_list[username]['game']['location'][0]-1250 < client_list[cli]['game']["location"][0] <client_list[username]['game']['location'][0]+1250 \
            and client_list[username]['game']['location'][1]-750 < client_list[cli]['game']["location"][1] <client_list[username]['game']['location'][1]+750:

                in_proximity[cli] = client_list[cli]
                print("in proximity")
    return in_proximity


def make_string(nearby: dict) -> dict:
    for name in nearby:
        user = nearby[name]
        nearby[name] = f'{user["game"]["username"]}:{user["game"]["direction"]}:{user["game"]["attacking"]}:{user["game"]["location"]}:{user["game"]["hitbox"]}:{user["game"]["frame"]}'
    return nearby


def exists(username: str)-> bool:
    return username in client_list

def append(data: str) -> None:
    global data_list
    
    answers = data[0].decode().split(":")
    temp_list = data_list
    client_info = client_data.copy()
    client_list[answers[0]]= client_info.copy()
    client_info['game']['username'] = answers[0]
    client_info['game']['direction']= answers[1]
    client_info['game']['attacking'] = bool(answers[2])
    temp = ''
    temp = answers[3][1:-1]
    temp =  tuple(map(int, temp.split(',')))
    client_info['game']['location'] = temp
    client_info['game']['hitbox'] = answers[4]
    client_info['game']['frame'] = int(floor(float(answers[5])))
    client_info['conn']['ip'] = data[1][0]
    client_info['conn']['port'] = int(data[1][1])

# def append(data):
#     global info_list
#     temp = ''
#     answers = data[0].decode().split(":")
#     client_list[answers[0]]= temp_list
#     temp_list["username"] = answers[0]
#     temp_list["direction"] = answers[1]
#     temp_list = info_list
#     temp_list["attacking"] = answers[2]
#     temp = answers[3][1:-1]
#     temp =  tuple(map(int, temp.split(',')))
#     temp_list["location"] = temp
#     temp_list["hitbox"] = answers[4]
#     temp_list["frame"] = int(floor(float(answers[5])))
#     temp_list["connection"] = data[1]

def add_user(username: str) -> None:
    global data_list
    client_list[username]= data_list    

def iterate_users(nearby: dict,conn) -> None:
    for user in nearby:
        send(nearby[user],conn)


def send(ans,conn):
    udp_server.sendto(str.encode(ans), (conn[1][0],conn[1][1]))


def receive():
        msg = udp_server.recvfrom(1024)
        return msg


def main():
    thread = threading.Thread(target=chat_server.main)
    thread.daemon = True
    thread.start()
    while True:

        data = receive()
        append(data)
        print(data[1][0])
        nearby = proximity(data[0].decode().split(":")[0])
        nearby = make_string(nearby)
        iterate_users(nearby,data)


if __name__ == "__main__":
    main()
    