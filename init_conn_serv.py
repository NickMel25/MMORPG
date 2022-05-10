from ipaddress import v4_int_to_packed
from random import randrange

from pygame import init
import encryption
import socket
import threading
# import udp_server
from Crypto.PublicKey import RSA
import db_access
import copy
class Init_conn_serv:

    def __init__(self,sclient_list,sclient_data) -> None:
        self.port = 14175
        self.ip = '0.0.0.0'
        self.server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_connection.bind((self.ip,self.port))

        self.client_list = sclient_list
        self.client_data = sclient_data
    
    
    def close_connection(self):
        self.server_connection.close()


    def connecting(self):
        self.server_connection.listen()
        conn, addr = self.server_connection.accept()
        return conn, addr


    def thread_handler(self,conn,addr) -> None:
        # try:
            redo = True
            while redo:
                answer = conn.recv(1024*4).decode()
                mode,username,password,confirmpassword = answer.split(":")
                if mode == 'login':
                    result = db_access.login(username,password)
                if mode == 'signup':
                    result = db_access.signup(username,password,confirmpassword)

                if result == 'Signup completed' or result == 'Correct password':
                    user_data = db_access.load(username)
                    answer = result+":"+':'.join([str(value) for value in user_data])
                    redo = False
                elif mode == 'login' and (result == 'Incorrect password' or result == 'User not found' or result == 'Name too long'):
                    answer = 'Incorrect username or password:'
                elif mode == 'signup' and (result == 'Username or Password cant be empty' or result == 'Password mismatch' or result == 'Invalid characters' or result == 'Username too long' or result == 'Username taken') :
                    answer = result+":"
                

                conn.sendall(answer.encode())

            # username = user_data[0]
            # dis = self.client_data.deepcopy()
            # dis = copy.deepcopy(self.client_data)
            self.client_list[username] = {{},{}}
            self.client_list[username]['conn']['ip'] = addr[0]
            self.client_list[username]['game']['username'] = username
            self.client_list[username]['game']['health'] = user_data[1]
            self.client_list[username]['game']['mana'] = user_data[2]
            self.client_list[username]['game']['location'] = (user_data[3],user_data[4])
            self.client_list[username]['game']['attack'] = user_data[5]
            self.client_list[username]['game']['bamboo'] = user_data[7]
            self.client_list[username]['game']['bloodpotion'] = user_data[8]
            self.client_list[username]['game']['spiritinabottle'] = user_data[9]
            self.client_list[username]['game']['coins'] = user_data[10]

            # dis['conn']['ip'] = addr[0]
            # dis['game']['username'] = username
            # dis['game']['health'] = user_data[1]
            # dis['game']['mana'] = user_data[2]
            # dis['game']['location'] = (user_data[3],user_data[4])
            # dis['game']['attack'] = user_data[5]
            # dis['game']['bamboo'] = user_data[7]
            # dis['game']['bloodpotion'] = user_data[8]
            # dis['game']['spiritinabottle'] = user_data[9]
            # dis['game']['coins'] = user_data[10]           
            # self.client_list[username] = dis 
            conn.close()
        # except ValueError as e:

            conn.close()
            return
        # except ConnectionResetError as e:
            conn.close()
            return
        


    def main(self) -> None:
        while True:
            conn,addr = self.connecting()
            thread = threading.Thread(target=self.thread_handler,args=[conn,addr])
            thread.daemon = True
            thread.start()


def mains():
    init_conn = Init_conn_serv({},{})
    init_conn.main()

if __name__ == "__main__":
    mains()