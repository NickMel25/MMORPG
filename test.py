import mysql.connector
cnn = mysql.connector.connect(user='root', password='Shmulik1234',host='localhost',database='mmo_cyber')
crsr = cnn.cursor()
query = "UPDATE players SET password = %s WHERE username = 'Ben';"
value = ('$argon2id$v=19$m=65536,t=3,p=4$Q+EpLKmll1s0V1U+Vb+rig$xo010+6GliMobCUUz0VYrHFkZOZrLkeeBqJh4RBCGU4',)
crsr.execute(query,value)
cnn.commit()
list = crsr.fetchall()

for x in list:
    print(x)