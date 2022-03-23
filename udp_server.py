from cgi import print_form
from http import client
from math import floor
import socket


ip = '0.0.0.0'
port = 13372
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((ip,port))
client_list = {}
client_time = {}
print(ip)




def proximity(username):
    in_proximity = {}
    print(client_list[username]["location"])
    for cli in client_list:
        if not (cli == username):
            if  client_list[username]["location"][0]-1250 < client_list[cli]["location"][0] <client_list[username]["location"][0]+1250 \
            and client_list[username]["location"][1]-750 < client_list[cli]["location"][1] <client_list[username]["location"][1]+750:
         
                in_proximity[cli] = client_list[cli]
                print("in proximity")
    return in_proximity


def make_string(nearby):
    for name in nearby:
        user = nearby[name]
        nearby[name] = f'{user["username"]}:{user["direction"]}:{user["attacking"]}:{user["location"]}:{user["hitbox"]}:{user["frame"]}'
    return nearby


def exists(username):
    return username in client_list


def append(data):
    temp = ''
    answers = data[0].decode().split(":")
    info_list = {}
    client_list[answers[0]]= info_list
    info_list["username"] = answers[0]
    info_list["direction"] = answers[1]
    info_list["attacking"] = answers[2]
    temp = answers[3][1:-1]
    temp =  tuple(map(int, temp.split(',')))
    info_list["location"] = temp
    info_list["hitbox"] = answers[4]
    info_list["frame"] = int(floor(float(answers[5])))
    info_list["connection"] = data[1]



def iterate_users(nearby,conn):
    for user in nearby:
        send(nearby[user],conn)


def send(ans,conn):
    udp_server.sendto(str.encode(ans), (conn[1][0],conn[1][1]))


def receive():
        msg = udp_server.recvfrom(1024)
        return msg


def main():
    while True:
        data = receive()
        append(data)
        
        nearby = proximity(data[0].decode().split(":")[0])
        nearby = make_string(nearby)
        iterate_users(nearby,data)

if __name__ == "__main__":
    main()
    