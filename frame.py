from mysql.connector import connect
from tabulate import tabulate
from getpass import getpass

conn=connect(host='localhost',user='root',passwd='Fawaz@33448113',database='hospital')

cur=conn.cursor()

cur.execute("create table if not exists users (id int auto_increment primary key,\
            name varchar(30) not null, email varchar(100) unique not null,pwd varchar(20) not null,\
            type enum('patient','doctor','admin') )")

cur.execute("create table if not exists patients (p_id int auto_increment primary key, user_id int ,\
            gender varchar(20),address varchar(200),age int,foreign key(user_id) references users(id) )")

cur.execute("create table if not exists doctors (d_id int auto_increment primary key, user_id int,\
            specialization varchar(100),phone varchar(15),foreign key(user_id) references users(id))")

def create_user():
  role = input("Enter role (patient/doctor/admin): ").lower()

  if role not in ("patient", "doctor", "admin"):
    print("Invalid role!")
    return
  name = input("name: ")
  password = getpass("Password: hidden ")
  email=input("email address: ")


  cur.execute("INSERT INTO users (name,email, pwd, type) VALUES (%s, %s, %s,%s)", 
                       (name,email, password, role))
  conn.commit()
  user_id = cur.lastrowid 

  if role == "patient":
    age = int(input("Age: "))
    gender = input("Gender (M/F): ")      
    address = input("Address: ")
    cur.execute("INSERT INTO patients (user_id, gender, address, age) VALUES (%s, %s, %s, %s)", (user_id, gender,address,age))
    conn.commit()

    cur.execute("select a.id,a.name,b.age,b.gender,a.email from users a  \
                join patients b on a.id=b.user_id\
                where user_id= %s",(user_id,))
    data=cur.fetchall()
    header=[i[0] for i in cur.description]
    print(tabulate(data,headers=header,tablefmt='pretty'))

  elif role== "doctor" :
    specialization = input("Specialization: ")
    phone = input("Phone: ")
    cur.execute("INSERT INTO doctors (user_id, specialization, phone) VALUES (%s, %s, %s) ", (user_id, specialization, phone))      
    conn.commit()
      
    cur.execute("select a.id,a.name,b.specialization,b.phone,a.email from users a \
                join doctors b on a.id=b.user_id \
                where user_id= %s",(user_id,))
    data=cur.fetchall()
    header=[i[0] for i in cur.description]
    print(tabulate(data,headers=header,tablefmt='pretty'))  

  elif role == "admin":
    secret = getpass("Enter admin creation key: *ENCRYPTED* ")
    if secret != "hms@admin":
      print("Invalid admin key. Rolling back...")
      cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
      conn.commit()
      return
    print(f'''admin succesfully created...
    user_id-{user_id} name-{name}''')
create_user()