from argon2 import PasswordHasher, exceptions
import mysql.connector
#connecting to database
login_conn = mysql.connector.connect(user='pass',host='localhost',password='pass1nfo',database='mmorpg',autocommit=True)
    
def close_conn():
    login_conn.close()

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

def main():
    username = input("please input username\n")
    password = input("please input password\n")
    login(username,password)
    close_conn()

if __name__ == '__main__':
    main()