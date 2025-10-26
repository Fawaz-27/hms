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
      role=login.login()

      if role=='patient':
        menu.patient_menu()
      elif role=='doctor':
        menu.doctor_menu()
      elif role=='admin':
        menu.admin_menu()
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