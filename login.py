from mysql.connector import connect
from tabulate import tabulate
from getpass import getpass

conn = connect(host='localhost', user='root', passwd='Fawaz@33448113', database='hospital')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(30) NOT NULL,
                dob DATE NOT NULL,
                gender ENUM('f','m') NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                pwd VARCHAR(255) NOT NULL,
                type ENUM('p','d','a','r') DEFAULT 'p')""")
def register_user():
    role_codes = {'a': 'admin', 'd': 'doctor', 'r': 'receptionist', 'p': 'patient'}
    role = input("Enter role (p=patient, d=doctor, a=admin, r=receptionist): ").lower()
    if role not in role_codes:
        print("Invalid role.")
        return
    if role in {'a','d','r'}:
        code = getpass(f"Enter code for {role_codes[role]}: ")
        valid_codes = {'a': 'admin', 'd': 'doctor', 'r': 'receptionist'}
        if code != valid_codes[role]:
            print("Invalid code.")
            return
    valid = False
    while not valid:
        name = input("Enter full name: ")
        dob = input("Enter date of birth (yyyy-mm-dd): ")
        gender = input("Enter gender (m/f): ")
        email = input("Enter email address: ")
        pwd = getpass("Enter password: ")
        if name and dob and gender and email and pwd:
            valid = True
        else:
            print("Invalid value in some field. Try again.")
    sql = """INSERT INTO users (name, dob, gender, email, pwd, type)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    vals = (name, dob, gender, email, pwd, role)
    cur.execute(sql, vals)
    conn.commit()
    select_sql = """SELECT id, name, dob, gender, email, type
                    FROM users
                    WHERE email=%s"""
    cur.execute(select_sql, (email,))
    data = cur.fetchall()
    header = [i[0] for i in cur.description]
    print(tabulate(data, headers=header, tablefmt='pretty'))
register_user()