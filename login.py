from mysql.connector import connect, Error
from getpass import getpass

try:
  conn = connect(host='localhost', user='root', passwd='Fawaz@33448113', database='hospital')
  cur = conn.cursor()
  
  def login():
    user=input("enter user id: ")
    pwd=getpass("enter password: HIDDEN")

    cur.execute(" SELECT pwd from users where id = %s",(user,))
 
    if cur.fetchone() is None:
      print('user id entered is invalid')
      return
    elif pwd == cur.fetchone()[0]:
      cur.execute("SELECT type from users where id=%s",(user,))
      return cur.fetchone()[0],user
    else:
      print('incorrect pwd')
      return 
  def update():
    pass
  
except Error as e:
  print(f"Connection error: {e}")

finally:
  try:
    cur.close()
    conn.close()
  except:
    pass 