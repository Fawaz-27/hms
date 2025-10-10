from mysql.connector import connect, Error
from tabulate import tabulate
from getpass import getpass

conn = connect(host = 'localhost', user = 'root', passwd = 'pass', database = 'hospital')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS inventory (
            item_id INT AUTO_INCREMENT PRIMARY KEY,
            item_name VARCHAR(100) NOT NULL,
            quantity INT NOT NULL DEFAULT 0,
            added_by INT FOREIGN KEY (added_by) REFERENCES users(id))""")

def login():
    email = input("Enter email : ")
    password = getpass("Enter password (hidden) : ")
    cur.execute("select id, type from users where email = %s and pwd = %s", (email,password))
    data = cur.fetchall()
    if not data:
        print("Invalid credentials!")
        return None, None
    return data[0][0], data[0][1]

def view_item():
    cur.execute("select i.item_id, i.item_name, i.quantity, u.name as added_by from inventory i join users u on i.added_by = u.id")

def inventory_menu(role, user_id):
    while True:
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
            elif choice == 2:
                view_item()
            elif choice == 3:
                break
        if role == 'd':
            print("\n 1. Request Item \n 2. View Inventory \n 3. Exit")
            choice = int(input("Enter choice : " ))
            if choice == 1:
                item_id = int(input("Enter item ID to request : "))
                quantity = int(input("Enter quantity to request : "))
                cur.execute("select quantity from inventory where item_id = %s", (item_id))
                data = cur.fetchall()
                if not data:
                    print("Not available!")
                elif data[0][0] < quantity:
                    print(f"Only {data[0][0]} stock available! \n Accept the available stock? (y/n) : ")
                    try:
                        choice = input().lower()
                        if choice == 'y':
                            new_quantity = int(input("Enter quantity to accept : "))
                            cur.execute("inventory set quantity = quantity - %s where item_id = %s", (new_quantity, item_id))
                            conn.commit()
                            print("Item will be issued soon.")
                        elif choice == 'n':
                            print("Request cancelled.")
                        else:
                            print("Invalid choice.")
                    except Error as e:
                        print(f"Error : {e}")
            if choice == 2:
                view_item()
            elif choice == 3:
                break