from mysql.connector import connect
from tabulate import tabulate
from getpass import getpass

conn=connect(host='localhost',user='root',passwd='Fawaz@33448113',database='hospital')

cur=conn.cursor()

cur.execute("create table if not exists users (id int auto_increment primary key,\
            name varchar(30) not null,dob date not null,gender enum('f','m') not null,\
            email varchar(100) unique not null,pwd varchar(20) not null,type enum('p','d','a','r') default 'p' )")

def register_patient():
  valid=False
  while not valid:
    name=input('enter your name: ')
    dob=input('enter your date of birth(yyyy-mm-dd): ')
    gender=input('enter your gender (m,f): ')
    email=input('Enter your email address: ')
    pwd=getpass('enter a password for your acc : ')
    if name and dob and gender and email and pwd :
      valid=True
    else:
      print('invalid value in some field...pls try again')

  cur.execute("insert into users (name,dob,gender,email,pwd) values (%s,%s,%s,%s,%s)",(name,dob,gender,email,pwd))
  conn.commit()
  cur.execute("select id,name,dob,gender,email from users where email='{}'".format(email))
  data=cur.fetchall()
  header=[i[0] for i in cur.description]
  print(tabulate(data,headers=header,tablefmt='pretty'))  

def register_admin():
  pass
