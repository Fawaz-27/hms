from mysql.connector import connect, Error
from tabulate import tabulate
from getpass import getpass

try:
  conn = connect(host='localhost', user='root', passwd='Fawaz@33448113', database='hospital')
  cur = conn.cursor()
  cur.execute("""CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY,
              name VARCHAR(30) NOT NULL, email VARCHAR(100) UNIQUE NOT NULL,
              pwd VARCHAR(255) NOT NULL, type ENUM('patient','doctor','admin'))""")
  cur.execute("""CREATE TABLE IF NOT EXISTS patients (p_id INT AUTO_INCREMENT PRIMARY KEY,
              user_id INT, gender VARCHAR(20), address VARCHAR(200), age INT,
              FOREIGN KEY (user_id) REFERENCES users(id))""")
  cur.execute("""CREATE TABLE IF NOT EXISTS doctors (d_id INT AUTO_INCREMENT PRIMARY KEY,
              user_id INT, specialization VARCHAR(100), phone VARCHAR(15),
              FOREIGN KEY (user_id) REFERENCES users(id))""")

  def create_user():
    role = input("Enter role (patient/doctor/admin): ").lower()
    if role not in ("patient", "doctor", "admin"):
      print("Invalid role!")
      return
    name = input("Enter name: ")
    email = input("Enter email address: ")
    password = getpass("Enter password (hidden): ")
    try:
      cur.execute("INSERT INTO users (name, email, pwd, type) VALUES (%s, %s, %s, %s)", (name, email, password, role))
      conn.commit()
      user_id = cur.lastrowid
      if role == "patient":
        age = int(input("Enter age: "))
        gender = input("Enter gender (M/F): ")
        address = input("Enter address: ")
        cur.execute("INSERT INTO patients (user_id, gender, address, age) VALUES (%s, %s, %s, %s)", (user_id, gender, address, age))
        conn.commit()
        cur.execute("SELECT a.id,a.name,b.age,b.gender,a.email FROM users a JOIN patients b ON a.id=b.user_id WHERE a.id=%s", (user_id,))
        data = cur.fetchall()
        header = [i[0] for i in cur.description]
        print("Patient account created successfully!")
        print(tabulate(data, headers=header, tablefmt='pretty'))
      elif role == "doctor":
        specialization = input("Enter specialization: ")
        phone = input("Enter phone number: ")
        cur.execute("INSERT INTO doctors (user_id, specialization, phone) VALUES (%s, %s, %s)", (user_id, specialization, phone))
        conn.commit()
        cur.execute("SELECT a.id,a.name,b.specialization,b.phone,a.email FROM users a JOIN doctors b ON a.id=b.user_id WHERE a.id=%s", (user_id,))
        data = cur.fetchall()
        header = [i[0] for i in cur.description]
        print("Doctor account created successfully!")
        print(tabulate(data, headers=header, tablefmt='pretty'))
      elif role == "admin":
        secret = getpass("Enter admin creation key (hidden): ")
        if secret != "hms@admin":
          print("Invalid admin key. Rolling back...")
          cur.execute("DELETE FROM users WHERE id=%s", (user_id,))
          conn.commit()
          return
        print(f"Admin account successfully created! User ID: {user_id} Name: {name}")
    except Error as e:
      print(f"Database error: {e}")
      conn.rollback()

except Error as e:
  print(f"Connection error: {e}")

finally:
  try:
    cur.close()
    conn.close()
  except:
    pass 