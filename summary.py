from mysql.connector import connect,Error
from tabulate import tabulate
from datetime import date, datetime

try:
  conn=connect(host='localhost',user='root',passwd='Fawaz@33448113',database='hospital')

  cur=conn.cursor()

  def view_patients():
    pass
  def view_doctors():
    pass
  def revenue_sum():
    pass

except Error as e:
  print("connection error",e)