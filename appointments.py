from mysql.connector import connect,Error
from tabulate import tabulate

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
      cur.execute('SELECT d_id as doctor_id ,specialization from doctors')
      header = [i[0] for i in cur.description]
      data=cur.fetchall()
      print(tabulate(data, headers=header, tablefmt='pretty'))
      doc_id=int(input('enter the doctor id for appointment.'))
      date=input("Enter date of appointment (YYYY-MM-DD): ")
      try:
        cur.execute("INSERT INTO appointments(u_id,d_id,date) VALUES (%s,%s,%s)",(user,doc_id,date))
      except Error as e:
        print('invalid doctor id or date format',e)
        return
      print('appointment have been added,pls check later for updates')
      conn.commit()
      
    def schedule_appointments(user):
      cur.execute("SELECT u_id as patient_id,date from appointments where d_id=%s and status='waiting",(user,))
      header = [i[0] for i in cur.description]
      data=cur.fetchall()
      print(tabulate(data, headers=header, tablefmt='pretty'))
      pat_id=int(input("enter patient id : "))
      ch=input('''1)schedule
                   2)remove''').lower()
      if ch == '1' or ch=='schedule':
        time=input("Enter time for appointment (HH:MM): ")
        try:
          cur.execute("update appointments set time=%s,status='scheduled' where p_id=%s",(time,pat_id))
        except Error as e:
          print('invallid patient id or time format')
          return 
      elif ch=='2' or ch=='remove':
        cur.execute('delete from appointments where p_id=%s',(pat_id,))
      else:
        print('enter valid option (1,2) or (schedule,remove)')
      conn.commit()

    def check_appointments(user):
      cur.execute("SELECT a_id,date,time from appointments where u_id =%s and status='scheduled'",(user,))
      header = [i[0] for i in cur.description]
      data=cur.fetchall()
      if data is None:
        print('your appointment have been removed...try another one at a diff date')
      else:
        print(tabulate(data, headers=header, tablefmt='pretty'))

  
  except Error as e:
    print(f"Database error: {e}")
except Error as e:
  print(f"connection error: {e}")