from mysql.connector import connect, Error
from tabulate import tabulate
from getpass import getpass

conn = connect(host = 'localhost', user = 'root', passwd = 'Fawaz@33448113', database = 'hospital')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS inventory (
            item_id INT AUTO_INCREMENT PRIMARY KEY,
            item_name VARCHAR(100) NOT NULL,
            quantity INT NOT NULL DEFAULT 0,
            added_by INT,
            FOREIGN KEY (added_by) REFERENCES users(id)
            )""")


def view_item():
  cur.execute("select i.item_id, i.item_name, i.quantity, u.name as added_by from inventory i join users u on i.added_by = u.id")
  data=cur.fetchall()
  print(tabulate(data,headers=['item_id','item_name','quantity','added_by'],tablefmt="pretty"))

def add_item(user_id):
  item_name = input("Enter item name : " )
  quantity = int(input("Enter quantity : " ))
  cur.execute("insert into inventory (item_name, quantity, added_by) values (%s, %s, %s)", (item_name, quantity, user_id))
  conn.commit()
  print("Item added successfully!")

def request_item():
  item_id = int(input("Enter item ID to request : "))
  quantity = int(input("Enter quantity to request : "))
  cur.execute("select quantity from inventory where item_id = %s", (item_id,))
  data = cur.fetchall()
  if not data:
    print("Not available!")
  elif data[0][0] < quantity:
    print(f"Only {data[0][0]} stock available! \n Accept the available stock? (y/n) : ")
    try:
      choice = input().lower()
      if choice == 'y':
        new_quantity = int(input("Enter quantity to accept : "))
        cur.execute("UPDATE inventory SET quantity = quantity - %s WHERE item_id = %s", (new_quantity, item_id))
        conn.commit()
        print("Item will be issued soon.")
      elif choice == 'n':
        print("Request cancelled.")
      else:
        print("Invalid choice.")
    except Error as e:
      print(f"Error : {e}")