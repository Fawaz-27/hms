from mysql.connector import connect,Error
from tabulate import tabulate
from getpass import getpass

try:
  conn=connect(host='localhost',user='root',passwd='Fawaz@33448113',database='hospital')

  cur=conn.cursor()
  try:
    cur.execute(''' CREATE TABLE IF NOT EXISTS appointments 
                (a_id int auto_increment primary key,u_id int,d_id int
                date date,time time,status enum('waiting','scheduled') default 'waiting')
                FORIEGN KEY (p_id) references patients(p_id)
                FORIEGN KEY (d_id) referneces doctors(d_id)''')

    def book_appointment(user):
      pass
  except Error as e:
    print(f"Database error: {e}")
except Error as e:
  print(f"connection error: {e}")