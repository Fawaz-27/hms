import appointments
import billing
import inventory

def patient_menu():
  print('''1)book an appointment
        2)check appointment detail
        3)billing details
        4)pay due
        5)view test results''')

def doctor_menu():
  print('''1)schedule appointments
        2)view inventory
        3)request item
        4)generate bill
        5)script test results''')

def admin_menu():
  print('''1)view all doctors
        2)view all patients
        3)view inventory
        4)add item
        5)view summary revenue''')