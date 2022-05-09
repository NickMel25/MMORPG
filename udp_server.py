from math import floor
import socket
import threading
from  init_conn_serv import Init_conn_serv
from chat_server import Chat_server
from end_conn_serv import End_conn_serv
import encryption
import atexit
print(socket.gethostbyname(socket.gethostname()))
ip = '0.0.0.0'
port = 10001
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
init_conn_serv = None
chat_server = None
end_conn_serv = None

client_time = {'attack':0,'hit':0,"movement":0}
data_list = {'username':'','direction':'','attacking':'','location':'','hitbox':'','frame':'','bamboo':0,'bloodpotion':0,'spiritinabottle':0,'coins':0,'health':0,'mana':0,'attack':0}
client_conn = {'ip':'',"port":0,"pubkey":'','seckey':'','pad_char':''}
client_data = {'game':data_list.copy(),"timers":client_time.copy(),'conn':client_conn.copy()}
client_list = {}

def get_client_list() -> dict:
    return client_list,client_data.copy()


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
    
    
    answers = data.split(":")
    temp_list = data_list
    # client_info = client_data.copy()
    # client_list[answers[0]]= client_info.copy()
    client_info = client_list[answers[0]]
    client_info['game']['username'] = answers[0]
    client_info['game']['direction']= answers[1]
    client_info['game']['attacking'] = bool(answers[2])
    temp = ''
    temp = answers[3][1:-1]
    temp =  tuple(map(int, temp.split(',')))
    client_info['game']['location'] = temp
    client_info['game']['hitbox'] = answers[4]
    client_info['game']['frame'] = int(floor(float(answers[5])))
    client_info['game']['bamboo'] = int(answers[6])
    client_info['game']['bloodpotion'] = int(answers[7])
    client_info['game']['spiritinabottle'] = int(answers[8])
    client_info['game']['coins'] = int(answers[9])


def add_user(username: str) -> None:
    global data_list
    client_list[username]= data_list    


def iterate_users(nearby: dict,conn) -> None:
    for user in nearby:
        send(nearby[user],conn)


def send(ans,conn):
    username = [k for k, v in client_list.items() if v['conn']['ip'] == conn[0]][0]
    encrypted_ans = encryption.symmetric_encrypt_message(ans, client_list[username]['conn']['seckey'], client_list[username]['conn']['pad_char'])
    udp_server.sendto(encrypted_ans, (conn[1][0],conn[1][1]))


def receive():
    msg, conn = udp_server.recvfrom(1024)
    username, msg = msg.decode().split(" ")
    if not username in client_list:
        return False
    decrypted_msg = encryption.symmetric_decrypt_message(msg, client_list[username]['conn']['seckey'], client_list[username]['conn']['pad_char'])
    return decrypted_msg


def main():
    global udp_server, init_conn_serv, end_conn_serv, chat_server, client_list, client_data
    
    udp_server.bind((ip,port))
    
    init_conn_serv = Init_conn_serv(client_list,client_data)
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

    while True:
        data = receive()
        if data:
            append(data)
            print(data[1][0])
            nearby = proximity(data.split(":")[0])
            nearby = make_string(nearby)
            iterate_users(nearby,data)


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
    