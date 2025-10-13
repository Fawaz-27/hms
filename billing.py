from mysql.connector import connect,Error
from tabulate import tabulate


try:
  conn=connect(host='localhost',user='root',passwd='Fawaz@33448113',database='hospital')

  cur=conn.cursor()
  try:
    cur.execute(''' CREATE TABLE IF NOT EXISTS billing 
                (bill_id int auto_increment primary key,p_id int,d_id int,total_amt int,
                days int,room int,test int,date date default curdate(),
                time time default curtime(),status enum('pending','paid') default 'pending')
                FORIEGN KEY (p_id) references patients(p_id)
                FORIEGN KEY (d_id) referneces doctors(d_id)''')
    
    def generate_bill(user):
      pat_id=int(input("enter patient id: "))
      stay_days=int(input('enter no of days stayed: '))
      room_fee=int(input('enter room fee: '))
      cur.execute("select con_fee from doctors where d_id=%s",(user,))
      consul_fee=cur.fetchone[0]
      test_fee=None#for now
      total_amt=stay_days*room_fee + consul_fee + test_fee

      cur.execute('''insert into billing (p_id,d_id,total_amt,days,room,test) 
                  values (%s,%s,%s,%s,%s,%s)''',(pat_id,user,total_amt,stay_days,room_fee,test_fee))
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