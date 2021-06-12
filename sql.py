from getpass import getpass
import MySQLdb as mysql
import os

def primer():
    clean = '-----------------------------------------'
    print(clean)
    print('Usage :-')
    print('1. add "todo item"  # Add a new todo')
    print('2. ls               # Show remaining todos')
    print('3. delete "name"    # Delete a todo')
    print('4. done "name"      # Complete a todo')
    print('5. help             # Show usage')
    print('6. report           # Statistics')
    print('7. clear            # Clear Window')
    print('8. exit             # Exit Program')
    print(clean)

def command(inp):
    if inp == 'help':
        return 'help',None

    elif inp == 'clear':
        return 'clear',None

    elif inp[0:6] == 'report':
        query = "select * from todo"
        return 'report',query

    elif inp[0:4] == 'done':
        item = inp[6:-1]
        query = "update todo set status=1 where name={}".\
                format("\""+str(item)+"\"")
        return "done",query

    elif inp[0:6] == 'delete':
        item = inp[8:-1]
        query = "delete from todo where name={}".\
                format("\""+str(item)+"\"")
        return "delete",query

    elif inp[0:3] == 'add':
        item = inp[5:-1]
        query = "insert into todo(name,status) values({},{})".\
                format("\""+str(item)+"\"",0)
        return "add",query

    elif inp[0:2] == 'ls':
        query = "select * from todo where status=0"
        return "ls",query

connection = mysql.connect(host='localhost',database="manage",\
        user='mukul',password="maiza")

# Create todo table
cursor = connection.cursor()
create_table = "create table if not exists todo(name char(50),status int)"
cursor.execute(create_table)

clean = '-------------------------------'

# Taking the input
primer()
while (inp := input("Command: "))!='exit' :
    cursor = connection.cursor()
    c = command(inp)
    if c[0] == 'help':
        primer()

    elif c[0] == 'clear':
        os.system('clear')

    elif c[0] == 'add':
        print(clean)
        cursor.execute(c[1])
        connection.commit()
        print("Todo Added Succesfully")
        print(clean)

    elif c[0] == 'delete':
        print(clean)
        cursor.execute(c[1])
        connection.commit()
        print("Todo Deleted Succesfully")
        print(clean)

    elif c[0] == 'report':
        print(clean)
        cursor.execute(c[1])
        rows = cursor.fetchall()
        count = len(rows)
        for i in range(1,count+1):
            if rows[i-1][1] == 0:
                print('['+str(i)+']',rows[i-1][0])
            else:
                strike = lambda x:'\u0336'.join(x) + '\u0336'
                print('[x]',strike(rows[i-1][0]))

        print(clean)

    elif c[0] == 'done':
        print(clean)
        cursor.execute(c[1])
        connection.commit()
        print("Todo Updated Succesfully")
        print(clean)

    elif c[0] == 'ls':
        print(clean)
        print("Remaining Todos:-")
        cursor.execute(c[1])
        rows = cursor.fetchall()
        count = len(rows)
        for i in range(1,count+1):
            print('['+str(i)+']',rows[i-1][0])
        print(clean)

cursor.close()
connection.close()
