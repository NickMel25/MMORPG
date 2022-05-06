from random import randrange
import encryption
import socket
import threading
from Crypto.PublicKey import RSA
import db_access
from connection import *
def end_conn():
    port = 57141
    ip = socket.gethostbyname(socket.gethostname())
    client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_connection.connect((ip,port))
    result = ''
    while result != "Completed successfully":
        result = client_connection.recv(1024*4)
        result = encryption.symmetric_decrypt_message(result,secret_key,pad_char)
        print(result)
    return result

