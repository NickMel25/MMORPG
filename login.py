from argon2 import PasswordHasher
import mysql.connector


def login(username,password):
    #connecting to database
    cnn = mysql.connector.connect(user='root',host='localhost',password='Shmulik1234',database='mmo_cyber')
    crsr = cnn.cursor()

    ph = PasswordHasher()
    
    #sql query
    query = 'SELECT password FROM players WHERE username=%s'
    crsr.execute(query,username)
    userpassword = crsr.fetchall()
    
    #checking username existence
    if userpassword:
        (userpassword,) = userpassword
    else:
        print("user not found")
        return
    
    try: #checking if passwords match
        ph.verify(userpassword[0],password)
        print("correct password") 
    except:
        print("Incorrect password")
    
    # if ph.check_needs_rehash(hash): Not sure if to add it and I dont know even how to lol
    #     userpassword = cnn.set_password_hash(username)

def main():
    username = input("please input username\n")
    username = (username,)
    print(username[0])
    password = input("please input password\n")
    login(username,password)

if __name__ == '__main__':
    main()