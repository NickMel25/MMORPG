from argon2 import PasswordHasher, exceptions
import mysql.connector 


# usage: close all database connections
def close_conn():
    signup_conn.close()
    login_conn.close()
    update_conn.close()
    update_conn.close()
    load_conn.close()
    


signup_conn = mysql.connector.connect(user='init', password='1n1t1al1zeuser',host='localhost',database='mmorpg',autocommit=True)

# input: username (str), password (str), confirm_password (str)
# output: instructions (str)
# usage: create user by standards: name 1 - 15 length & without special characters (except _),username not taken, passwords match, all parameters are not null. 
def signup(username: str,password: str,confirm_password: str) -> str :
    # validity check    
    username = username.strip()
    password = password.strip()
    confirm_password = confirm_password.strip()
    if not username or not password or not confirm_password:
        print("Username or Password cant be null")
        return "Username or Password cant be empty"
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
    
    with signup_conn.cursor() as signup_cursor:
    # trying to create user
        try:
            signup_cursor.callproc("createUser",[username,password])
            signup_conn.commit()
            print("Signup completed")
            return "Signup completed"
        except mysql.connector.errors.IntegrityError:
            print("Username already taken")
            return "Username taken"
        except mysql.connector.errors.DataError:
            print("Username too long")
            return "Username too long"


login_conn = mysql.connector.connect(user='pass',host='localhost',password='pass1nfo',database='mmorpg',autocommit=True)

# input: username (str), password (str)
# output: instructions (str)    
# usage: validate login 
def login(username: str,password: str) -> str:
    
    username = username.strip()
    password = password.strip()
    # login_cursor = login_conn.cursor()
    with login_conn.cursor() as login_cursor:
        ph = PasswordHasher()
        userpassword = ''
        #sql query
        try:
            login_cursor.callproc("passwordByUser",[username,])     
            userpassword = login_cursor.stored_results()
        except mysql.connector.errors.DatabaseError as e:
            print(e)
            return "Name too long"

        #checking username existence
        try:
            userpassword = [r.fetchall() for r in login_cursor.stored_results()][0][0][0]
        except IndexError:
            print("User not found")
            return "User not found"
        
        try: #checking if passwords match
            ph.verify(userpassword,password)
            print("correct password") 
            return "Correct password"
        except exceptions.VerifyMismatchError:
            print("Incorrect password")
            return "Incorrect password"
        
        # if ph.check_needs_rehash(hash): # Not sure if its needed and I dont know even how to
        #     userpassword = ph.set_password_hash(username)


update_conn = mysql.connector.connect(user='renew',host='localhost',password='renew1nfo',database='mmorpg',autocommit=True)

# input: username (str), data (list)
# output: instructions (str)
# usage: update user info by data given
def update(username: str,data: list) -> str:

    username = username.strip()
    
    with update_conn.cursor() as update_cursor:
        try:
            update_cursor.callproc('updateData',[username] + data)
            update_conn.commit()
            
        except mysql.connector.errors.DataError as e:
            print("Username too long")
            return "Username too long"


load_conn = mysql.connector.connect(user='view',host='localhost',password='v1ew1nfo',database='mmorpg',autocommit=True)

# input: username (str)
# output: instruction (str) or data (tuple)
# usage: load data on specific user    
def load(username: str) -> str or tuple:
    username = username.strip()
    
    with load_conn.cursor() as load_cursor:
        try:
            load_cursor.callproc('selectInfo',[username,])
            return [r.fetchall() for r in load_cursor.stored_results()][0][0] 
        except mysql.connector.errors.DataError as e:
            print("Username too long")
            return "Username too long"
        except IndexError as e:
            print("User not found")
            return "User not found"


def main():
    pass

if __name__ == "__main__":
    main()

