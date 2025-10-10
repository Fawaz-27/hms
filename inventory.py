from mysql.connector import connect, Error
from tabulate import tabulate
from getpass import getpass

conn = connect(host = 'localhost', user = 'root', passwd = 'pass', database = 'hospital')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS inventory (
            item_id INT AUTO_INCREMENT PRIMARY KEY,
            item_name VARCHAR(100) NOT NULL,
            quantity INT NOT NULL DEFAULT 0,
            added_by INT FOREIGN KEY REFERENCES users(id))""")

def login():
    email = input("Enter email : ")
    password = getpass("Enter password (hidden) : ")
    cur.execute("select id, type from users where email = %s and pwd = %s", (email,password))
    data = cur.fetchall()
    if not data:
        print("Invalid credentials!")
        return None, None
    return data[0], data[1]

def inventory_menu(role):   
    print("\n Inventory Management Menu ")
    if role == 'a':
        print("\n 1. Add Item \n 2. View Inventory \n 3. Exit")
        choice = int(input("Enter choice : " ))
        if choice == 1:
            item_name = input("Enter item name : " )
            quantity = int(input("Enter quantity : " ))
            cur.execute("insert into inventory (item_name, quantity, added_by) values (%s, %s, %s)", (item_name, quantity, user_id))
            conn.commit()
            print("Item added successfully!")
        if choice == 2:
            cur.execute("select * from inventory")
            data = cur.fetchall()