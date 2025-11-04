from mysql.connector import connect, Error
from tabulate import tabulate
from getpass import getpass

try:
  conn = connect(host='localhost', user='root', passwd='Fawaz@33448113', database='hospital')
  cur = conn.cursor()
  cur.execute("""CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY,
              name VARCHAR(30) NOT NULL, email VARCHAR(100) UNIQUE NOT NULL,
              password VARCHAR(255) NOT NULL, type ENUM('patient','doctor','admin'))""")
  cur.execute("""CREATE TABLE IF NOT EXISTS patients (p_id INT AUTO_INCREMENT PRIMARY KEY,
              user_id INT, gender VARCHAR(20), address VARCHAR(200), age INT, staff ENUM('yes', 'no') DEFAULT 'no',
              status ENUM('active', 'inactive') DEFAULT 'active',
              FOREIGN KEY (user_id) REFERENCES users(id))""")
  cur.execute("""CREATE TABLE IF NOT EXISTS doctors (d_id INT AUTO_INCREMENT PRIMARY KEY,
              user_id INT, specialization VARCHAR(100), phone VARCHAR(15), con_fee INT,
              status ENUM('active', 'inactive') DEFAULT 'active',
              FOREIGN KEY (user_id) REFERENCES users(id))""")
  cur.execute("""CREATE TABLE IF NOT EXISTS update_requests (request_id INT AUTO_INCREMENT PRIMARY KEY,
              doctor_id INT NOT NULL, field VARCHAR (50) NOT NULL, new VARCHAR(100) NOT NULL, 
              status ENUM('pending', 'approved' ,'rejected') DEFAULT 'pending',
              FOREIGN KEY (doctor_id) REFERENCES users(id))""")
  cur.execute("""CREATE TABLE IF NOT EXISTS logs (log_id INT AUTO_INCREMENT PRIMARY KEY, 
              user_id INT NOT NULL, field VARCHAR(50) NOT NULL, old_value VARCHAR(100), new_value VARCHAR(100),
              FOREIGN KEY (user_id) REFERENCES users(id))""")

  
except Error as e:
  print(f"Connection error: {e}")

def create_user():
    print("Medical personnel must register a patient account prior to using any hospital services intended for their personal use.")
    while True:
        role = input("Enter role (patient/doctor/admin): ").lower()
        if role not in ("patient", "doctor", "admin"):
            print("Invalid role!")
            continue
        name = input("Enter name: ")
        email = input("Enter email address: ")
        while True:
            pwd = getpass("Enter password (hidden) : ")
            password = getpass("Re-enter password (hidden) : ")
            if pwd != password:
                print("The passwords do not match!")
                continue
            break
        try:
            cur.execute("INSERT INTO users (name, email, password, type) VALUES (%s, %s, %s, %s)", (name, email, password, role))
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
                doctor_is_patient(user_id)
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

def modify_user(user_id):
  while True:
    cur.execute("SELECT type FROM users WHERE id = %s", (user_id,))
    data = cur.fetchone()
    if not data:
       print("User not found!")
       return
    role = data[0]
    if role == 'patient':
      print("1) Update name\n2) Update email\n3) Update password\n4) Update age\n5) Update gender\n6) Update address\n7) Exit")
      while True:
        try:
          ch = int(input("Enter choice : "))
          if ch not in range(1,8):
            print("Invalid choice!")
            continue
        except ValueError:
          print("Enter a valid integer!")
          continue
        break
      if ch == 1:
        cur.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        old_name = cur.fetchone()[0]
        name = input("Enter new name : ")
        cur.execute("UPDATE users SET name = %s WHERE id = %s", (name, user_id))
        cur.execute("INSERT INTO logs (user_id, field, old_value, new_value) VALUES (%s, %s, %s, %s)", (user_id, 'name', old_name, name))
      elif ch == 2:
        cur.execute("SELECT email FROM users WHERE id = %s", (user_id,))
        old_email = cur.fetchone()[0]
        email = input("Enter new email : ")
        cur.execute("UPDATE users SET email = %s WHERE id = %s", (email, user_id))
        cur.execute("INSERT INTO logs (user_id, field, old_value, new_value) VALUES (%s, %s, %s, %s)", (user_id, 'email', old_email, email))
      elif ch == 3:
        pwd = getpass("Enter new password (hidden) : ")
        while True:
          password = getpass("Re-enter new password (hidden) : ")
          if pwd != password:
            print("The passwords do not match!")
            continue
          break
        cur.execute("UPDATE users SET password = %s WHERE id = %s", (password, user_id))
      elif ch == 4:
        cur.execute("SELECT age FROM patients WHERE user_id = %s", (user_id,))
        old_age = cur.fetchone()[0]
        age = int(input("Enter new age : "))
        cur.execute("UPDATE patients SET age = %s WHERE user_id = %s", (age, user_id))
        cur.execute("INSERT INTO logs (user_id, field, old_value, new_value) VALUES (%s, %s, %s, %s)", (user_id, 'age', old_age, age))
      elif ch == 5:
        cur.execute("SELECT gender from patients WHERE user_id = %s", (user_id,))
        old_gender = cur.fetchone()[0]
        gender = input("Enter new gender (Male/Female/Other) : ")
        while True:
          gender_c = input(f"Are you sure you're {gender}? (y/n)").lower()
          if gender_c == 'y':
            break
          elif gender_c == 'n':
            gender = input("Enter new gender (Male/Female/Other) : ")
          else:
            print("Invalid choice.")
        if gender == 'Attack Helicopter' :
          cur.execute("UPDATE users SET type = 'admin' WHERE id = %s", (user_id,))
        cur.execute("UPDATE patients SET gender = %s WHERE user_id = %s", (gender, user_id))
        cur.execute("INSERT INTO logs (user_id, field, old_value, new_value) VALUES (%s, %s, %s, %s)", (user_id, 'gender', old_gender, gender))
      elif ch == 6:
        cur.execute("SELECT address FROM patients WHERE user_id = %s", (user_id,))
        old_address = cur.fetchone()[0]
        address = input("Enter new address : ")
        cur.execute("UPDATE patients SET address = %s WHERE user_id = %s", (address, user_id))
        cur.execute("INSERT INTO logs (user_id, field, old_value, new_value) VALUES (%s, %s, %s, %s)", (user_id, 'address', old_address, address))
      elif ch == 7:
        break
      conn.commit()
    elif role == 'doctor':
      doctor_requests(user_id)
      break

def doctor_is_patient(user_id):
    cur.execute("SELECT d.user_id FROM doctors d JOIN patients p ON d.user_id = p.user_id WHERE d.user_id = %s", (user_id,))
    if cur.fetchone():
        cur.execute("UPDATE patients SET staff = 'yes' WHERE user_id = %s", (user_id,))
        conn.commit()

def doctor_requests(user_id):
    requests = []
    while True:
        field = input("Enter field to update (name, email, password, specialization, phone, consultation fee) or exit : ").lower()
        if field == 'exit':
            break
        if field not in ['name', 'email', 'password', 'specialization', 'phone', 'consultation fee']:
            print("Invalid field!")
            continue

        if field == 'consultation fee':
            db_field = 'con_fee'
            while True:
                try:
                    value = int(input("Enter new value : "))
                    break
                except ValueError:
                    print("Enter a valid integer!")
        else:
            db_field = field
            value = input(f"Enter new value for {field} : ")

        requests.append((user_id, db_field, value))

    for i in requests:
        cur.execute("INSERT INTO update_requests (doctor_id, field, new) VALUES (%s, %s, %s)", i)
    conn.commit()
    print("Your request(s) have been submitted for review.")

def admin_review():
    cur.execute("SELECT * from update_requests where status = 'pending'")
    data = cur.fetchall()
    if not data:
        print("No pending requests.")
        return
    for i in data:
        request_id, doctor_id, field, new_value, status = i
        print(f"Request ID: {request_id}, Doctor ID: {doctor_id}, Field: {field}, New Value: {new_value}")
        while True:
            decision = input("Approve (a) / Reject (r) : ").lower()
            if decision not in {'a', 'r'}:
                print("Invalid choice!")
                continue
            break
        if decision == 'a':
            table = 'users' if field in ['name', 'email', 'password'] else 'doctors'
            column = 'id' if table == 'users' else 'user_id'

            cur.execute(f"UPDATE {table} SET {field} = %s WHERE {column} = %s", (new_value, doctor_id))
            cur.execute("UPDATE update_requests SET status = 'approved' WHERE request_id = %s", (request_id,))
            print(f"Request ID {request_id} approved.")
        else:
            cur.execute("UPDATE update_requests SET status = 'rejected' WHERE request_id = %s", (request_id,))
            print(f"Request ID {request_id} rejected.")
        conn.commit()