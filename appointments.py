from mysql.connector import connect,Error
from tabulate import tabulate
from datetime import datetime

try:
  conn=connect(host='localhost',user='root',passwd='Fawaz@33448113',database='hospital')

  cur=conn.cursor()
  try:
    cur.execute('''CREATE TABLE IF NOT EXISTS appointments (
                a_id INT AUTO_INCREMENT PRIMARY KEY, p_id INT, d_id INT,
                date DATE,time TIME,status ENUM('waiting','scheduled') DEFAULT 'waiting',
                FOREIGN KEY (p_id) REFERENCES patients(p_id),
                FOREIGN KEY (d_id) REFERENCES doctors(d_id)
                )''')

    def book_appointment(user_id):
      spec = input("Please enter the doctor's specialization you want to book an appointment with : ")
      cur.execute('''select d_id as doctor_id, specialization, name from doctors join users on doctors.user_id = users.id
                  where specialization = %s''', (spec,))
      header = [i[0] for i in cur.description]
      data = cur.fetchall()
      if not data:
        print("No doctors found with that specialization!")
        return
      print(tabulate(data, headers = header, tablefmt = 'pretty'))
      doc_id = int(input("Enter the doctor ID you want to book an appointment with : "))
      if doc_id not in [i[0] for i in data]:
        print("Invalid doctor ID!")
        return
      try:
        date_str = input("Enter date for appointment (YYYY-MM-DD): ")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        print("Valid date:", date)
        cur.execute('INSERT INTO appointments (p_id, d_id, date) VALUES (%s, %s, %s)',(user_id, doc_id, date))
        conn.commit()
      except ValueError:
        print("Invalid date! Please use YYYY-MM-DD format.")
        return
      print("Appointment book request submitted. Please check back later.")
      
    def schedule_appointments(user):
      cur.execute("SELECT p_id as patient_id, date, a_id FROM appointments where d_id=%s and status='waiting'",(user,))
      header = [i[0] for i in cur.description]
      data=cur.fetchall()
      print(tabulate(data, headers=header, tablefmt='pretty'))
      pat_id=int(input("enter patient id : "))
      ch=input('''1) schedule
                  2) remove''').lower()
      if ch == '1' or ch=='schedule':
        time=input("Enter time for appointment (HH:MM): ")
        try:
          cur.execute("update appointments set time=%s,status='scheduled' where p_id=%s",(time,pat_id))
        except Error as e:
          print('invalid patient id or time format:', e)
          return 
      elif ch=='2' or ch=='remove':
        cur.execute('delete from appointments where p_id=%s',(pat_id,))
      else:
        print('enter valid option (1,2) or (schedule,remove)')
      conn.commit()

    def check_appointments(user):
      cur.execute("SELECT a_id,date,time from appointments where p_id =%s and status='scheduled'",(user,))
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