
from init_conn_client import *
from end_conn_client import *
from chat_client import *
from udp_client import *

class Connection:
    def __init__(self,ip) -> None:
        
        self.init_conn_client = Init_conn_client(ip)
        keys = self.init_conn_client.get_keys()
        
        self.end_conn_client = End_conn_client(ip, keys[0], keys[1], keys[2], keys[3], keys[4])
        
        self.chat_client = Chat_client(ip, keys[0], keys[1], keys[2], keys[3], keys[4])
        
        self.udp_client = Udp_client(ip, keys[0], keys[1], keys[2], keys[3], keys[4])

    def close_con(self):
        try:
            self.init_conn_client.close_connection()
            self.udp_client.close_connection()
            self.chat_client.close_connection()
        except Exception as e:
            return