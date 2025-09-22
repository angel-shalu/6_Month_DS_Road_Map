import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', password='2005', database='internshipdb')
mycursor = conn.cursor()

# Create table only if it doesn't exist
mycursor.execute('create table if not exists student(name varchar(50), branch varchar(10), id int)')

# Show all databases
mycursor.execute('show tables')

for x in mycursor:
    print(x)
