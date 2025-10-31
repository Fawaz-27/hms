import appointments
import billing
import inventory
import tests


def patient_menu(user_id):
  while True:
    print("1) Book an appointment")
    print("2) Check appointment detail")
    print("3) Billing details")
    print("4) Pay due")
    print("5) Order test")
    print("6) View test")
    print("7) Exit")
    try:
      choice = int(input("Enter choice: "))
    except ValueError:
      print("Enter a number between 1 and 7")
      continue

    if choice == 1:
      try:
        appointments.book_appointment(user_id)
      except Exception as e:
        print("Error booking appointment:", e)
    elif choice == 2:
      try:
        appointments.check_appointments(user_id)
      except Exception as e:
        print("Error checking appointments:", e)
    elif choice == 3:
      try:
        billing.view_bill(user_id)
      except Exception as e:
        print("Error viewing billing:", e)
    elif choice == 4:
      try:
        billing.pay(user_id)
      except Exception as e:
        print("Error paying bill:", e)
    elif choice == 5:
      try:
        tests.order_test(user_id)
      except Exception as e:
        print("Error ordering test:", e)
    elif choice==6:
      try:
        tests.view_test(user_id)
      except Exception as e:
        print("Error viewing test:", e)
    elif choice == 7:
      break
    else:
      print("Invalid choice")


def doctor_menu(doctor_id):

  while True:
    print("1) Schedule appointments")
    print("2) View inventory")
    print("3) Request item")
    print("4) Generate bill")
    print("5) Prescribe / script test results")
    print("6) Exit")
    try:
      choice = int(input("Enter choice: "))
    except ValueError:
      print("Enter a number between 1 and 6")
      continue

    if choice == 1:
      try:
        appointments.schedule_appointments(doctor_id)
      except Exception as e:
        print("Error scheduling appointments:", e)
    elif choice == 2:
      try:
        inventory.view_item()
      except Exception as e:
        print("Error viewing inventory:", e)
    elif choice == 3:
      try:
        inventory.request_item()
      except Exception as e:
        print("Error requesting item:", e)
    elif choice == 4:
      try:
        billing.generate_bill(doctor_id)
      except Exception as e:
        print("Error generating bill:", e)
    elif choice == 5:
      try:
        tests.review_test()
      except Exception as e:
        print("Error reviewing test", e)
    elif choice == 6:
      break
    else:
      print("Invalid choice")


def admin_menu(admin_id):
  while True:
    print("1) View all doctors ")
    print("2) View all patients ")
    print("3) View inventory")
    print("4) Add item")
    print("5) View summary revenue ")
    print("6) Add test")
    print("7) Exit")
    try:
      choice = int(input("Enter choice: "))
    except ValueError:
      print("Enter a number between 1 and 6")
      continue

    if choice == 1:
      print("View all doctors: not implemented yet.")
    elif choice == 2:
      print("View all patients: not implemented yet.")
    elif choice == 3:
      try:
        inventory.view_item()
      except Exception as e:
        print("Error viewing inventory:", e)
    elif choice == 4:
      try:
        inventory.add_item(admin_id)
      except Exception as e:
        print("Error adding item:", e)
    elif choice == 5:
      print("View summary revenue: not implemented yet.")
    elif choice == 6:
      print("View summary revenue: not implemented yet.")
    elif choice == 7:
      break
    else:
      print("Invalid choice")