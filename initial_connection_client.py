import encryption
import socket
from settings import *
from Crypto.PublicKey import RSA
import connection

port = 14175
ip = socket.gethostbyname(socket.gethostname())
client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_connection.connect((ip,port))


def init():
    private_client_key,public_client_key = encryption.assymetric_generate_keys()
    client_connection.sendall(public_client_key.publickey().exportKey())
    print("tryting to receive public key")
    public_server_key = client_connection.recv(1024*4)
    public_server_key = RSA.importKey(public_server_key, passphrase=None) 
    print("tryting to receive secret key")
    secret_key = client_connection.recv(1024*4)
    secret_key = encryption.assymetric_decrypt_message(secret_key,private_client_key)
    print("tryting to receive pad char")
    pad_char = client_connection.recv(1024*4)
    print("all complete")
    pad_char = encryption.assymetric_decrypt_message(pad_char,private_client_key)
    pad_char = pad_char.decode()
    confirmation_message = 'confriming data recievement'
    encrypted_confirmation_message = encryption.symmetric_encrypt_message(confirmation_message,secret_key,pad_char)
    client_connection.sendall(encrypted_confirmation_message)

    connection.set_conn(private_client_key,public_client_key,public_server_key,secret_key,pad_char)
    # connection.public_client_key = public_client_key
    # connection.public_server_key = public_server_key
    # connection.private_client_key = private_client_key
    # connection.secret_key = secret_key
    # connection.pad_char = pad_char
  


def user_connection( mode:str, username :str,password :str,confirmpassword = '') -> list:
    message = f"{mode}:{username}:{password}:{confirmpassword}"
    encrypted_message = encryption.symmetric_encrypt_message(message,connection.secret_key,connection.pad_char)
    client_connection.sendall(encrypted_message)
    encrypted_result = client_connection.recv(1024*4)
    result = encryption.symmetric_decrypt_message(encrypted_result,connection.secret_key,connection.pad_char)
    print(result)
    return result.split(":")


def main():
    init()
# if __name__ == "__main__":
#     main()
