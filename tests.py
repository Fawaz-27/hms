from mysql.connector import connect, Error
from tabulate import tabulate
from datetime import date, datetime

try:
    conn = connect(host = 'localhost', user = 'root', password = 'mimimimi', database = 'hospital')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tests (
                test_id INT AUTO_INCREMENT PRIMARY KEY,
                test_name VARCHAR(50) NOT NULL,
                test_cost INT NOT NULL)''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY, 
                test_id INT NOT NULL, 
                p_id INT NOT NULL,
                order_date DATE,
                status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
                FOREIGN KEY (test_id) REFERENCES tests(test_id),
                FOREIGN KEY (p_id) REFERENCES users(id))''')
    
    def order_test(id):
        cur.execute("SELECT test_id, test_name, test_cost FROM tests")
        header = [i[0] for i in cur.description]
        data = cur.fetchall()
        print(tabulate(data, headers = header, tablefmt = 'pretty'))
        while True:
            test_id = int(input("Enter Test ID to order : "))
            if test_id not in [i[0] for i in data]:
                print("Invalid Test ID!")
            break
        date_today = date.today()
        cur.execute("INSERT INTO orders (test_id, p_id, order_date) VALUES (%s, %s, %s)", (test_id, id, date_today))
        conn.commit()
        print("Test ordered successfully. Wait for updates.")

    def view_test(id):
        cur.execute('''SELECT o.order_id, t.test_name, t.test_cost, o.order_date, o.status
                    FROM orders o JOIN tests t ON o.test_id = t.test_id
                    where o.p_id = %s''', (id,))
        header = [i[0] for i in cur.description]
        data = cur.fetchall()
        if not data:
            print("No tests ordered yet.")
        else:
            print(tabulate(data, headers = header, tablefmt = 'pretty'))

except Error as e:
    print(f"Database connection error : {e}")