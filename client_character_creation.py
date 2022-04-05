from queue import Empty
from argon2 import PasswordHasher
import mysql.connector

#create connection and cursor with database and input the values needed
cnn = mysql.connector.connect(user='root', password='Shmulik1234',host='localhost',database='mmo_cyber')
crsr = cnn.cursor()

def validity_check(username,password):
    
    #username length check
    if len(username)>15:
        print("username too long")
        return False

    #character validation check (by ascii)
    for c in username:
        print(c)
        print(ord(c))
        if not (47<ord(c)<57 or 64<ord(c)<91 or 96<ord(c)<123 or ord(c) == 95) :
            print("contains invalid characters")
            return False
    
    #checks if username is already taken
    query = "SELECT username FROM players where username =%s"
    value = (username,)
    crsr.execute(query,value)
    ans = crsr.fetchall()
    if ans:
        print("username already taken")
        return False    
    
    
    #hashing password
    ph = PasswordHasher()
    hash = ph.hash(password)
    #verifying password
    passconfirm = input("Please verify your password")
    try:
        ph.verify(hash,passconfirm)
    except: # could not catch for some reason the real exception: argon2.exceptions.VerifyMismatchError
        print("Passwords did not match")
        return False

    return create_character(username,hash)

def create_character(username,password):

    #sql query
    query = 'INSERT INTO players (username, password) VALUES (%s, %s)'
    values = (username,password)
    try:
        crsr.execute(query,values)
    except mysql.connector.IntegrityError:
        print("Something is wrong, please try again")
        return False
    cnn.commit()
    return True




def main():

    while True:
        username = input("Enter your username")
        password = input("Enter your password")
        username = username.strip()

        
        if validity_check(username, password):
            break
        print("username already taken")
    print("user successfully created!")
if __name__ == '__main__':
    main()


