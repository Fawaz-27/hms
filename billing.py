from mysql.connector import connect,Error
from tabulate import tabulate
from datetime import date, datetime


try:
  conn=connect(host='localhost',user='root',passwd='Fawaz@33448113',database='hospital')

  cur=conn.cursor()
  try:
    cur.execute('''CREATE TABLE IF NOT EXISTS billing (
        bill_id INT AUTO_INCREMENT PRIMARY KEY,
        p_id INT, d_id INT, total_amt INT,
        days INT, room INT, test INT,
        bill_date DATE,
        bill_time TIME,
        status ENUM('pending','paid') DEFAULT 'pending',
        FOREIGN KEY (p_id) REFERENCES patients(p_id),
        FOREIGN KEY (d_id) REFERENCES doctors(d_id)
        )''')

    def generate_bill(user):
      pat_id=int(input("enter patient id: "))
      stay_days=int(input('enter no of days stayed: '))
      room_fee=int(input('enter room fee: '))
      cur.execute("select con_fee from doctors where d_id=%s",(user,))
      row = cur.fetchone()
      consul_fee = row[0] if row else 0
      cur.execute('''SELECT SUM(t.test_cost)
                FROM orders o JOIN tests t ON o.test_id = t.test_id
                where o.p_id = %s''', (user,))
      row = cur.fetchone()
      test_fee =  row[0] if row else 0
      total_amt = stay_days * room_fee + consul_fee + test_fee
      bill_date = date.today()
      bill_time = datetime.now().time()

      cur.execute('''insert into billing (p_id,d_id,total_amt,days,room,test,bill_date,bill_time) 
                  values (%s,%s,%s,%s,%s,%s,%s,%s)''',(pat_id,user,total_amt,stay_days,room_fee,test_fee,bill_date,bill_time))
      conn.commit()

    def view_bill(user):
      cur.execute("select * from billing where p_id=%s",(user,))
      header = [i[0] for i in cur.description]
      data=cur.fetchall()
      print(tabulate(data, headers=header, tablefmt='pretty'))

    def pay(user):
      cur.execute("select * from billing where p_id=%s",(user,))
      data = cur.fetchall()
      sum=0
      for i in data:
        if i[-1]=='pending':
          sum+= i[3]
      print(f"amount pending:{sum} ")
      confirm=input('would you like to pay (y/n): ').lower()
      if confirm=='y':
        cur.execute("update billing set status='paid' where p_id=%s",(user,))
        conn.commit()
        print("bill paid successfully.\namt due=0")
      else:
        print(f"amt due={sum}")
  except Error as e:
    print(f"Database error: {e}")
except Error as e:
  print(f"connection error: {e}")