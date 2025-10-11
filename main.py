from mysql.connector import connect,Error
from tabulate import tabulate
from getpass import getpass
from colorama import Fore

import frame
import login

red=Fore.RED
green=Fore.GREEN

try:
  conn=connect(host='localhost',user='root',passwd='Fawaz@33448113',database='hospital')

  cur=conn.cursor()

  print(red,' WELCOME TO SAVELIVES HOSPITAL')
  while True:
    ch1=input(green,'''1)register
                  2)login
                  3)exit''')
    if ch1.lower() == '1' or ch1.lower() =='register':
      frame.create_user()
    
    elif ch1.lower()=='2' or ch1.lower() =='login':
      role=login.login()

      if role=='patient':
        pass
      elif role=='doctor':
        pass
      elif role=='admin':
        pass
      else:
        continue

    
    elif ch1.lower()=='3' or ch1.lower() =='exit':
      break
    
    else:
      print(red,"please enter a valid input (1,2,3) or (register,login,exit) ")
  
  print(green,'THANKYOU FOR USING SAVELIVES SERVICES!')


except Error as e:
  print(f"connection error:{e}")

finally:
  cur.close()
  conn.close()