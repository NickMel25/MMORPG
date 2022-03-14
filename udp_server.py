from http import client
import socket


ip = socket.gethostbyname(socket.gethostname())
port = 13372
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((ip,port))
client_list = {}
client_time = {}
print(ip)




def proximity(username):
    in_proximity = {}
    for user in client_list:
        if not (user == username):
            if  client_list[username][0]-1250 < client_list[user]["direction"][0]<client_list[username][0]+1250 and client_list[username][1]-750 < client_list[user]["direction"][1]-750<client_list[username][1]+750:
                in_proximity[user] = client_list[user]
    return in_proximity


def make_string(nearby):
    for name in nearby:
        user = nearby[name]
        nearby[name] = f'{user["username"]}:{user["direction"]}:{user["attacking"]}:{user["location"]}:{user["hitbox"]}'
    return nearby


def exists(username):
    return username in client_list


def append(data):
    answers = data[0].decode().split(":")
    info_list = {}
    client_list[answers[0]]= info_list
    info_list["username"] = answers[0]
    info_list["direction"] = answers[1]
    info_list["attacking"] = answers[2]
    info_list["location"] = answers[3]
    info_list["hitbox"] = answers[4]
    info_list["connection"] = data[1]
    print(info_list["username"])


def iterate_users(nearby,conn):
    for user in nearby:
        send(nearby[user],conn)


def send(ans,conn):
    udp_server.sendto(str.encode(ans), (conn[1][0],conn[1][1]))


def receive():
        msg = udp_server.recvfrom(1024)
        print(msg)
        return msg


def main():
    while True:
        data = receive()
        if not exists(data[0].decode().split(":")[0]):
            append(data)
        
        nearby = proximity(data[0].decode().split(":")[0])
        nearby = make_string(nearby)
        iterate_users(nearby,data)

if __name__ == "__main__":
    main()
    