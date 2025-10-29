from mysql.connector import connect,Error

import frame
import login
import menu

try:
  conn=connect(host='localhost',user='root',passwd='Fawaz@33448113',database='hospital')

  cur=conn.cursor()

  print('\033[4;34m WELCOME TO SAVELIVES HOSPITAL \033[0m')
  while True:
    ch=input('1)register\n2)login\n3)exit\nEnter a choice: ')
    if ch.lower() == '1' or ch.lower() =='register':
      frame.create_user()
    
    elif ch.lower()=='2' or ch.lower() =='login':
      role,uid=login.login()

      if role=='patient':
        cur.execute("select p_id from patients where user_id=%s",(uid,))
        p_id=cur.fetchone()[0]
        menu.patient_menu(p_id)
      elif role=='doctor':
        cur.execute("select d_id from doctors where user_id=%s",(uid,))
        d_id=cur.fetchone()[0]
        menu.doctor_menu(d_id)
      elif role=='admin':
        menu.admin_menu(uid)
      else:
        continue

    
    elif ch.lower()=='3' or ch.lower() =='exit':
      break
    
    else:
      print( " \033[31m please enter a valid input (1,2,3) or (register,login,exit) \033[0m")
  
  print('\033[1;32m THANKYOU FOR USING SAVELIVES SERVICES! \033[0m')


except Error as e:
  print(f"connection error:{e}")

finally:
  cur.close()
  conn.close()