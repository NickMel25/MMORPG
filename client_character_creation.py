from argon2 import PasswordHasher, exceptions
import mysql.connector

#create connection and cursor with database and input the values needed
create_conn = mysql.connector.connect(user='init', password='1n1t1al1zeuser',host='localhost',database='mmorpg',autocommit=True)


def close_conn():
    create_conn.close()

# input: username (str) and password (str), confirm_password (str)
# output: instructions (str)
def create_character(username: str,password: str,confirm_password: str) -> str :
    # validity check    
    username = username.strip()
    password = password.strip()
    #username length check
    if len(username)>15:
        print("Username too long")
        return "Username too long"
        

    #character validation check (by ascii)
    for c in username:
        if not (47<ord(c)<58 or 64<ord(c)<91 or 96<ord(c)<123 or ord(c) == 95) :
            print("Contains invalid characters")
            return "Invalid characters"
            
     
    #hashing password
    ph = PasswordHasher()
    password = ph.hash(password)
    #verifying password
    try:
        ph.verify(password,confirm_password)
    except exceptions.VerifyMismatchError: 
        print("Passwords did not match")
        return "Password mismatch"
    
    with create_conn.cursor() as create_cursor:
    # trying to create user
        try:
            create_cursor.callproc("createUser",[username,password])
            create_conn.commit()
        except mysql.connector.errors.IntegrityError:
            print("Username already taken")
            return "Username taken"
        except mysql.connector.errors.DataError:
            print("Username too long")
            return "Username too long"

def main():

        username = input("Enter your username\n")
        password = input("Enter your password\n")
        confirm_password = input("Confirm your password\n")
        create_character(username,password,confirm_password)
        close_conn()
        


if __name__ == '__main__':
    main()


