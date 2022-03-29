
import random 
str = 'testext'
op = ''
for i in range(len(str)):
    p =len(str)-i
    op+= str[len(str)-1:]
    str = str[:-1]
    print(op)
op = op[::-1]
print(op)

