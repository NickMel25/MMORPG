from random import randrange
import encryption
import socket
import threading
import udp_server
from Crypto.PublicKey import RSA
import db_access

port = 14175
ip = '0.0.0.0'
server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection.bind((ip,port))
private_key, public_key = encryption.assymetric_generate_keys()
username = 'wassap'
client_list = udp_server.client_list
def connecting():
    global chat_server
    server_connection.listen()
    conn, addr = server_connection.accept()
    return conn, addr

def thread_handler(conn,addr) -> None:
    # keys exchange and setup
    client_public_key = RSA.importKey(conn.recv(1024*4), passphrase=None) 
    conn.sendall(public_key.publickey().exportKey())
    secret_key = encryption.symmetric_generate_key()
    encrypted_secret_key = encryption.assymetric_encrypt_message(secret_key,client_public_key)
    conn.sendall(encrypted_secret_key)
    pad_char = chr(randrange(1,26)+96)
    encrypted_pad_char = encryption.assymetric_encrypt_message(pad_char.encode(),client_public_key)
    conn.sendall(encrypted_pad_char)
    print("pad char sent")
    confirmation_message = conn.recv(1024*4)
    confirmation_message = encryption.symmetric_decrypt_message(confirmation_message,secret_key,pad_char)
    print(confirmation_message)

    # login / signup validity
    redo = True
    while redo:
        encrypted_answer = conn.recv(1024*4)
        decrypted_answer = encryption.symmetric_decrypt_message(encrypted_answer,secret_key,pad_char)
        mode,username,password,confirmpassword = decrypted_answer.split(":")
        if mode == 'login':
            result = db_access.login(username,password)
        if mode == 'signup':
            result = db_access.signup(username,password,confirmpassword)
        print(result)

        if result == 'Signup completed' or result == 'Correct password':
            user_data = db_access.load(username)
            answer = result+":"+':'.join([str(value) for value in user_data])
            redo = False
        elif mode == 'login' and (result == 'Incorrect password' or result == 'User not found' or result == 'Name too long'):
            answer = 'Incorrect username or password:'
        elif mode == 'signup' and (result == 'Username or Password cant be empty' or result == 'Password mismatch' or result == 'Invalid characters' or result == 'Username too long' or result == 'Username taken') :
            answer = result+":"
        
        encrypted_result = encryption.symmetric_encrypt_message(answer,secret_key,pad_char)
        conn.sendall(encrypted_result)
        pass
    username = user_data[0]
    client_list[username] = udp_server.client_data.copy()
    client_list[username]['conn']['seckey'] = secret_key 
    client_list[username]['conn']['ip'] = addr[0]
    client_list[username]['conn']['port'] = addr[1]
    client_list[username]['conn']['pubkey'] = client_public_key
    client_list[username]['game']['health'] = user_data[1]
    client_list[username]['game']['mana'] = user_data[2]
    client_list[username]['game']['location'] = (user_data[3],user_data[4])
    client_list[username]['game']['attack'] = user_data[5]
    client_list[username]['game']['bamboo'] = user_data[7]
    client_list[username]['game']['bloodpotion'] = user_data[8]
    client_list[username]['game']['spiritinabottle'] = user_data[9]
    client_list[username]['game']['coins'] = user_data[10]
    pass

def end_conn():
    pass

def start_conn():
    while True:
        conn,addr = connecting()
        thread = threading.Thread(target=thread_handler,args=[conn,addr])
        thread.daemon = True
        thread.start()
        print("created new thread")

def main():
    thread = threading.Thread(target=start_conn)
    thread.daemon = True
    thread.start()
    # thread = threading.Thread(target=end_conn)
    # thread.daemon = True
    # thread.start()


if __name__ == "__main__":
    main()