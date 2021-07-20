import MySQLdb
import datetime

#change the username(root) and password(abcd1234) here to your own mysql username and password
db = MySQLdb.connect('localhost','localhost', 'abcd1234', 'CAFE')
cursor = db.cursor()

#initializing staffID
cursor.execute("""SELECT MAX(STAFF_ID) FROM STAFF;""")
resp = cursor.fetchone()
if resp[0] is None:
	staffID = 1
staffID = resp[0] + 1

#initializing foodID
cursor.execute("""SELECT MAX(FOOD_ID) FROM MENU;""")
resp = cursor.fetchone()
if resp[0] is None:
	foodID = 1;
foodID = resp[0] + 1

#initializing customerID
cursor.execute("""SELECT MAX(CUSTOMER_ID) FROM CUSTOMER;""")
resp = cursor.fetchone()
if resp[0] is None:
	customerID = 1;
else:
	customerID = resp[0] + 1

#initializing orderID
cursor.execute("""SELECT MAX(ORDER_ID) FROM `ORDERS`;""")
resp = cursor.fetchone()
if resp[0] is None:
	orderID = 1
else:
	orderID = resp[0] + 1

#initializing paymentID
cursor.execute("""SELECT MAX(PAYMENT_ID) FROM PAYMENT;""")
resp = cursor.fetchone()
if resp[0] is None:
	paymentID = 1
else:
	paymentID = resp[0] + 1

#initializing invoiceID
cursor.execute("""SELECT MAX(INVOICE_ID) FROM COMPLETE_INFO;""")
resp = cursor.fetchone()
if resp[0] is None:
	invoiceID = 1
else:
	invoiceID = resp[0] + 1

#function to add staff details into database
def addStaff():
	global staffID
	try:
		Fname = raw_input('Enter first name of employee: ')
		Lname = raw_input('Enter last name of employee: ')
		email = raw_input('Enter email of employee: ')
		address = raw_input('Enter address of employee: ')
		sex = raw_input('Enter sex of the staff. (M-Male / F-Female / O-Other): ')
		dob = raw_input('Enter DOB of employee: ')
		salary = int(raw_input('Enter the base salary: '))
		employeeType = int(raw_input('Enter employee type (0 for chef, 1 for waiter, 2 for manager): '))
		if employeeType != 0 and employeeType != 1 and employeeType !=  2:
			print 
			print ('Invalid employee type')
			print
			return

		mySql_insert_query = """INSERT INTO STAFF (STAFF_ID, FNAME, LNAME, EMAIL, ADDRESS, SEX, DOB, CATEGORY ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
		cursor.execute(mySql_insert_query, (staffID, Fname, Lname, email, address, sex, dob, employeeType))
		db.commit()

		mySql_insert_query = """INSERT INTO SALARY (STAFF_ID, BASE_SALARY, BONUS, DEDUCTIONS) VALUES (%s, %s, %s, %s)"""	
		cursor.execute(mySql_insert_query, (staffID, salary, 0, 0))
		db.commit()

		if employeeType == 0:
			wexp = int(raw_input('Enter WORK EXPERIENCE of chef in years: '))
			mySql_insert_query = """INSERT INTO CHEF (STAFF_ID, WORK_EXPERIENCE) VALUES (%s, %s)"""
			cursor.execute(mySql_insert_query, (staffID - 1, wexp))
		elif employeeType == 1:
			proflang = raw_input('Enter proficient language of waitor in years: ')
			mySql_insert_query = """INSERT INTO WAITER (STAFF_ID, LANGUAGE) VALUES (%s, %s)"""
			cursor.execute(mySql_insert_query, (staffID - 1, proflang))
		db.commit()

		while(1): 
			contactNumber = raw_input('Enter contact number of employee: ')
			if len(contactNumber) != 10:
				print 
				print ("Invalid contact number")
				return
			contactNumber = int(contactNumber)
			mySql_insert_query = """INSERT INTO STAFF_CONTACT (STAFF_ID, CONTACT_NUMBER ) VALUES (%s, %s)"""
			cursor.execute(mySql_insert_query, (staffID, contactNumber))
			db.commit()
			ch = raw_input("Enter Another contact number? (Y-Yes / N-No) : ")
			if ch == 'N' or ch == 'n' or ch == 'no' or ch == 'No' or ch == 'NO':
				break
		staffID = staffID + 1	
		print("Added Staff!!")
	except :
		print ("Error")
		db.rollback()

#function to delete staff details from database.
#Note that a staff details can't be deleted if he is involved in any relation like ordering or serving
def deleteStaff():
	try:
		empID = int(raw_input('Enter Staff ID of the staff whose details want to delete: '))
	except:
		print ("Invalid input")
		return
	cursor.execute("""SELECT * from STAFF WHERE STAFF_ID = %s;""", (empID,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print ('Invalid employee ID')
		return

	try:
		cursor.execute("""SELECT * from CHEF WHERE STAFF_ID = %s;""", (empID,))
		rowcount = cursor.rowcount
		if rowcount !=0:
			resp = cursor.fetchone()
			cursor.execute("""DELETE from CHEF WHERE STAFF_ID = %s;""", (empID,))
			cursor.execute("""DELETE from STAFF WHERE STAFF_ID = %s;""", (empID,))
			db.commit()

		cursor.execute("""SELECT * from WAITER WHERE STAFF_ID = %s;""", (empID,))
		rowcount = cursor.rowcount

		if rowcount !=0:
			cursor.execute("""SELECT * from WAITER WHERE STAFF_ID = %s;""", (empID,))
			resp = cursor.fetchone()
			cursor.execute("""DELETE from WAITER WHERE STAFF_ID = %s;""", (empID,))
			cursor.execute("""DELETE from STAFF WHERE STAFF_ID = %s;""", (empID,))
			db.commit()

		cursor.execute("""SELECT * from STAFF WHERE STAFF_ID = %s;""", (empID,))
		rowcount = cursor.rowcount
		if rowcount !=0:
			cursor.execute("""DELETE from STAFF_CONTACT WHERE STAFF_ID = %s;""", (empID,))
			cursor.execute("""DELETE from STAFF_ASSOCIATES WHERE STAFF_ID = %s;""", (empID,))
			cursor.execute("""DELETE from SALARY WHERE STAFF_ID = %s;""", (empID,))
			cursor.execute("""DELETE from STAFF WHERE STAFF_ID = %s;""", (empID,))
			db.commit()
		print("Details Deleted!!")
	except:
		print ("Since this Staff was involved in a relation,  we want to maintain its record. Hence we can't delete details of a staff who already prepared or served an order or managed someone.")
		return

#function to add an item into food menu
def addMenu():
	global foodID
	item=raw_input("Enter the name of food item: ")
	cursor.execute("""SELECT COUNT(*) FROM MENU WHERE NAME = %s;""",(item,))
	exists = cursor.fetchone()
	if exists[0] != 0:
		print
		print ("Item already exists")
		return
	
	try:
		about = raw_input("Enter about the food item: ")
		foodCat = raw_input("Enter the type of food item: ")
		price=float(raw_input("Enter its price: "))
	except:
		print ("Invalid input")
		return
	
	try:
		cursor.execute("""INSERT INTO MENU VALUES (%s,%s,%s,%s,%s,%s);""",(foodID,item,about,price,0,0))
		cursor.execute("""INSERT INTO FOOD_CATEGORY VALUES (%s,%s);""",(foodID,foodCat))
		db.commit()
		print ("Added new menu item")
		foodID=foodID+1
	except:
		print("Error!")
		db.rollback()

#function to delete a food item from menu.
#Note that if a food item has been ordered, we cannot remove it since we wish to maintain its record
def deleteMenu():
	try:
		food_id = int(raw_input('Enter Food ID of the item you want to remove: '))
		cursor.execute("""SELECT * from MENU WHERE FOOD_ID = %s;""", (food_id,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print ('\nInvalid food ID')
			return

		resp = cursor.fetchone()
		cursor.execute("""DELETE from FOOD_CATEGORY WHERE FOOD_ID = %s;""", (food_id,))
		cursor.execute("""DELETE from MENU WHERE FOOD_ID = %s;""", (food_id,))
		
		db.commit()

		print("REMOVED!!")
	except:
		print ("Cannot remove a food item that has been ordered since we wnat to maintain its record")
		db.rollback()


#function to change the price of a food item
def changePrice():
	item =  raw_input('Enter name of item whose price you want to change: ')
	cursor.execute("""SELECT COUNT(*) FROM MENU WHERE NAME = %s;""",(item,))
	exists = cursor.fetchone()
	if exists[0] == 0:
		print ("\nItem does not exist in the Menu")
		return

	try:
		price = int(raw_input('Enter new price: '))
	except:
		print ("Invalid input")
		return

	try:	
		cursor.execute("""UPDATE MENU SET PRICE = %s WHERE NAME = %s;""", (price, item,))
		db.commit()
		print
		print ("Price changed")

	except:
		print ("Error")
		db.rollback()

#function to add details of a customer to the database
def addCustomer():
	global customerID
	Fname = raw_input('Enter first name of customer: ')
	Lname = raw_input('Enter last name of customer: ')
	contactNo = int(raw_input('Enter contact number of customer: '))

	# table = cursor.fetchone()
	try:	
		mySql_insert_query = """INSERT INTO CUSTOMER (CUSTOMER_ID, FNAME, LNAME, CONTACT_NUMBER) VALUES (%s, %s, %s, %s)"""
		cursor.execute(mySql_insert_query, (customerID, Fname, Lname, contactNo))
		db.commit()
		customerID = customerID + 1
		print("Added!!")
	except:
		print ("Error")
		db.rollback()

#function to update details of a customer 
def updateCustomer():
	custid =  int(raw_input('Enter Customer ID whose details you want to change: '))
	try:
		cursor.execute("""SELECT * FROM `CUSTOMER` WHERE CUSTOMER_ID = %s;""",(custid,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print
			print ("No customer with this id")
			return
		
		contactNo = int(raw_input('Enter new contact number of customer: '))

		cursor.execute("""UPDATE CUSTOMER SET CONTACT_NUMBER = %s WHERE CUSTOMER_ID = %s;""", (contactNo, custid,))	
		db.commit()
		print("Updated!!")
	except:
		print ("Error")
		db.rollback()

#function to calculate the salary of an employee
def calcSalary():
	staff_id = raw_input('Enter STAFF_ID whose total salary you want to know: ')
	cursor.execute("""SELECT * FROM `SALARY` WHERE STAFF_ID = %s;""",(staff_id,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print
		print ("No staff with this id")
		return

	response = cursor.fetchone()
	totsal = response[1] + response[2] - response[3];
	print("Base Salary = " + str(response[1]) + "\nBonus = " + str(response[2]) + "\nDeductions = " + str(response[3]) + "\n-------------------\nTotal Salary = " + str(totsal))

#function to calculate average rating of a food item
def calcAvgRating():
	try:
		food_name = raw_input('Enter Name of food item whose rating you want to know: ')
		cursor.execute("""SELECT * FROM MENU WHERE NAME = %s;""",(food_name,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print
			print ("No food with this name")
			return
		response = cursor.fetchone()
		print("\n Rating = " + str(response[5]/response[4]))
	except:
		print ("Error")
		db.rollback()

#function to add Staff Dependent details
def addStaffDependent():
	try:
		stid=int(raw_input("Enter the staff id: "))
	except:
		print ("Invalid input")
		return

	cursor.execute("""SELECT * FROM STAFF WHERE STAFF_ID = %s;""",(stid,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print ("Invalid employee id")
		return

	emp = cursor.fetchone()
	edfname = raw_input("Enter associate's first name: ")
	edlname = raw_input("Enter associate's last name: ")
	edadd = raw_input("Enter associate's address: ")
	edcno = int(raw_input("Enter associate's contact no: "))
	try:
		cursor.execute("""SELECT * FROM STAFF_ASSOCIATES WHERE STAFF_ID = %s AND FNAME = %s AND LNAME = %s;""",(stid,edfname,edlname))
		rowcount = cursor.rowcount
		if rowcount != 0:
			print ("Dependent information already present")
			return

		mySql_insert_query = """INSERT INTO STAFF_ASSOCIATES (STAFF_ID, FNAME, LNAME, ADDRESS, CONTACT_NUMBER) VALUES (%s,%s,%s,%s,%s);"""
		cursor.execute(mySql_insert_query,(stid,edfname,edlname,edadd,edcno))
		db.commit()
		print("Added!!")
	except :
		print ("Error")
		db.rollback()

#function to search food item using food name as parameter
def searchFoodByName():
	try:
		foodname = raw_input("Enter the name of the food item you want to know about: ")
		cursor.execute("""SELECT * FROM MENU WHERE NAME = %s;""",(foodname,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print ("\nNo such food item.")
			return
		foodresp = cursor.fetchall()
		for response in foodresp:
			print("\nFOOD_ID = "+ str(response[0]))
			print("\nABOUT = "+ response[2])
			print("\nPRICE = "+ str(response[3]))
			print("\nAVG RATING = "+ str(response[5]/response[4]))
	except:
		print ("Error")
		db.rollback()

#function to search for all the food items of a particular category
def searchFoodByCategory():
	try:
		foodcat = raw_input("Enter the category of the food item you want to know about: ")
		cursor.execute("""SELECT * FROM FOOD_CATEGORY WHERE  CATEGORY = %s;""",(foodcat,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print ("\nNo food item of this category.")
			return
		foodresp = cursor.fetchall()
		for response in foodresp:
			cursor.execute("""SELECT * FROM MENU WHERE FOOD_ID = %s;""",(response[0],))
			foodname = cursor.fetchone()
			print(foodname[1]+"\n")
			print
	except:
		print("Error")
		db.rollback

#function to place order 
def placeOrder():
	global orderID
	global paymentID
	global invoiceID
	custoption = int(raw_input('Customer already a member or not? (1 for yes, 2 for no): '))

	if custoption == 2:
		addCustomer()

	try:
		custID = int(raw_input('Enter customer ID: '))
	except:
		print ("Invalid input")
		return


	cursor.execute("""SELECT * FROM CUSTOMER WHERE CUSTOMER_ID = %s;""", (custID,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print
		print ("Invalid customerID")
		return

	customer = cursor.fetchone()
	
	tabnum = int(raw_input("Enter table number : "))
	nowtime = datetime.datetime.now()
	nowtime = nowtime.strftime("%H:%M:%S")
	mySql_insert_query = """INSERT INTO COMPLETE_INFO (INVOICE_ID, CUSTOMER_ID, TABLE_NUMBER, TIME_OF_DAY, TOTAL_AMOUNT, STATUS) VALUES (%s,%s,%s,%s,%s,%s);"""
	cursor.execute(mySql_insert_query,(invoiceID, customer[0], tabnum, nowtime, 0, "PENDING"))
	db.commit()
	totamt = 0;
	while True:
		try:
			food_name  = raw_input("Enter name of food item: ")
			quantity = int(raw_input('Enter its quantity: '))
			discnt = int(raw_input('Enter discount: '))
		except:
			print ("Invalid input")
			return
		
		cursor.execute("""SELECT * FROM MENU WHERE NAME = %s;""", (food_name,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print
			print ("Invalid name")
			return
		
		food_resp = cursor.fetchone()
		cursor.execute("""SELECT * FROM CHEF ORDER BY RAND() LIMIT 1;""")
		chef_resp = cursor.fetchone()
		foodid = int(food_resp[0])
		chefid = int(chef_resp[0])
		rating = rateOrder(food_resp[1], quantity)

		mySql_insert_query = """INSERT INTO ORDERS (ORDER_ID, INVOICE_ID, FOOD_ID, STAFF_ID, DISCOUNT, QUANTITY, RATING) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
		cursor.execute(mySql_insert_query, (orderID, invoiceID, foodid, chefid, discnt, quantity, rating))
		db.commit()

		cursor.execute("""SELECT * FROM WAITER ORDER BY RAND() LIMIT 1;""")
		waiter_resp = cursor.fetchone()

		mySql_insert_query = """INSERT INTO ORDERING (CUSTOMER_ID, ORDER_ID) VALUES (%s,%s);"""
		cursor.execute(mySql_insert_query,(customer[0],orderID))
		db.commit()
		
		mySql_insert_query = """INSERT INTO SERVING (STAFF_ID, ORDER_ID) VALUES (%s,%s);"""
		cursor.execute(mySql_insert_query,(waiter_resp[0],orderID))
		db.commit()

		mySql_insert_query = """INSERT INTO PREPARING (STAFF_ID, ORDER_ID) VALUES (%s,%s);"""
		cursor.execute(mySql_insert_query,(chef_resp[0],orderID))
		db.commit()

		orderID = orderID + 1
		totamt = totamt + int(food_resp[3])*quantity - int(discnt)*quantity

		

		flag = raw_input(("Finish Ordering? (enter Y for Yes, N for No): "))	
		if flag == 'Y' or flag == 'y':
			break;

	cursor.execute("""UPDATE COMPLETE_INFO SET TOTAL_AMOUNT = %s WHERE INVOICE_ID = %s;""", (totamt, invoiceID,))
	db.commit()
	invoiceID = invoiceID + 1;

	print("Thank you for ordering!!")

#function to initiate the payment for any order
def makePayment():
	invID = int(raw_input("Enter the Invoice ID: "))
	try: 
		cursor.execute("""SELECT * FROM COMPLETE_INFO WHERE INVOICE_ID = %s;""", (invID,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print ("\nInvalid invoice ID")
			return
		invresp = cursor.fetchone()

		portal = raw_input("Enter Portal (CASH / CREDIT CARD / DEBIT CARD / PAYTM / GPAY / AMAZON PAY / OTHERS) : ")
		mySql_insert_query = """INSERT INTO PAYMENT (PAYMENT_ID, INVOICE_ID, AMOUNT, PORTAL) VALUES (%s,%s,%s,%s);"""
		cursor.execute(mySql_insert_query,(paymentID,invID, invresp[4],portal))
		db.commit()
		print
		cursor.execute("""UPDATE COMPLETE_INFO SET STATUS = %s WHERE INVOICE_ID = %s;""", ('PAID', invID,))
		db.commit()

		print("\nPAID\n")
	except:
		print("Error")
		db.rollback

#function to rate any food item that the customer has ordered
def rateOrder(foodname, quantity):
	# foodname = int(raw_input("Enter food name you want to rate : "))
	print("Rate this item:")
	cursor.execute("""SELECT * FROM MENU WHERE NAME = %s;""",(foodname,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print ("\nNo such food item.")
		return
	foodresp = cursor.fetchone()

	stars = int(raw_input("Enter number of stars: (1 or 2 or 3 or 4 or 5) : "))
	if stars > 5 or stars < 1:
		print("Invalid rating")
		return

	totrating = foodresp[5] + stars

	cursor.execute("""UPDATE MENU SET RATING = %s , NO_OF_TIMES_ORDERED = %s WHERE NAME = %s;""", (totrating, foodresp[4]+quantity, foodname,))
	db.commit()
	return stars

#function to show the most ordered item of the menu
def showMostOrdered():
	cursor.execute("""SELECT MAX(NO_OF_TIMES_ORDERED) FROM MENU;""")
	number = cursor.fetchone()
	cursor.execute("""SELECT NAME FROM MENU WHERE NO_OF_TIMES_ORDERED = %s;""", (number,))
	items = cursor.fetchall()

	for i in items:
		print(str(i[0])+"\n")

#function to rate food item
def rateOrder2():
	foodname = raw_input("Enter food name you want to rate : ")
	print("Rate this item: \n")
	cursor.execute("""SELECT * FROM MENU WHERE NAME = %s;""",(foodname,))
	rowcount = cursor.rowcount
	if rowcount == 0:
		print ("\nNo such food item.")
		return
	foodresp = cursor.fetchone()

	stars = int(raw_input("Enter number of stars: (1 or 2 or 3 or 4 or 5) : "))
	if stars > 5 or stars < 1:
		print("Invalid rating")
		return

	totrating = foodresp[5] + stars

	cursor.execute("""UPDATE MENU SET RATING = %s , NO_OF_TIMES_ORDERED = %s WHERE NAME = %s;""", (totrating, foodresp[4]+1, foodname,))
	db.commit()
	return

#function to set manager of a particular employee
def setManager():
	try:
		managerid = int(raw_input("Enter Manager - id : "))
		staff_id = int(raw_input("Enter Staff - id : "))
		# cursor.execute("""SELECT NAME FROM MENU WHERE NO_OF_TIMES_ORDERED = %s;""", (number,))

		cursor.execute("""SELECT STAFF_ID FROM STAFF WHERE STAFF_ID = %s AND CATEGORY = %s;""",(managerid,2,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print ("\nInvalid Manager ID.")
			return

		cursor.execute("""SELECT STAFF_ID FROM STAFF WHERE STAFF_ID = %s AND CATEGORY <> %s;""",(staff_id,2,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print ("\nInvalid Staff ID.")
			return

		mySql_insert_query = """INSERT INTO MANAGES (MANAGER_ID, STAFF_ID) VALUES (%s,%s);"""
		cursor.execute(mySql_insert_query,(managerid, staff_id))
		db.commit()

		print("Manager set!!")
	except:
		print("Error!")
		db.rollback()

#function to generate E-Invoice for an invoice
def generateEInvoice():
	try:
		invid = int(raw_input("Enter the invoice ID to generate E-Invoice: "))
		cursor.execute("""SELECT * FROM COMPLETE_INFO WHERE INVOICE_ID = %s;""", (invid,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print("Invalid Invoice ID.")
			return
		invoice = cursor.fetchone()

		cursor.execute("""SELECT * FROM PAYMENT WHERE INVOICE_ID = %s;""", (invid,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print("Payment for this inovice id still not made.")
			return

		paym = cursor.fetchone()

		cursor.execute("""SELECT * FROM ORDERS WHERE INVOICE_ID = %s;""", (invid,))
		orders = cursor.fetchall()
		i=1
		for order in orders:
			cursor.execute("""SELECT * FROM MENU WHERE FOOD_ID = %s;""", (order[2],))
			fooditem = cursor.fetchone()
			print(str(i) + ".\n\tItem = " + str(fooditem[1]) + "\n\tQuantity = " + str(order[5]) + "\n\tDiscount = " + str(order[4]) + "\n\tPrice per unit item = " + str(fooditem[3]) + "\n")
			mySql_insert_query = """INSERT INTO GENERATING_EINVOICE (CUSTOMER_ID, INVOICE_ID, PAYMENT_ID, ORDER_ID) VALUES (%s,%s,%s,%s);"""
			cursor.execute(mySql_insert_query,(invoice[1],invid, paym[0] ,order[0]))
			db.commit()
			i = i+1

		print("Total Amount = "+ str(invoice[4]))
		print("Paid by: " + paym[3])

		print("*****E-INVOICE GENERATED*****\n")

	except:
		print("Error!")
		db.rollback()


#function to edit staff details
def editStaffDetails():
	try:
		staffid =  int(raw_input('Enter Staff ID of the staff whose details you want to change: '))
		cursor.execute("""SELECT * FROM STAFF WHERE STAFF_ID = %s;""", (staffid,))
		rowcount = cursor.rowcount
		if rowcount == 0:
			print("Invalid Staff ID.")
			return
		print("1- Email")
		print("2- Address")
		print("3- Phone Number")
		print("4- Salary")
		print("5- Add Bonus")
		print("6- Add Deduction")

		ch = int(raw_input("Enter the detail you want to change"))
		if ch  > 0 and ch < 7:
			pass
		else:
			print("Invalid input")
			return

		if ch == 1:
			newmail = raw_input("Enter the new email id")
			cursor.execute("""UPDATE STAFF SET EMAIL = %s WHERE STAFF_ID = %s;""", (newmail, staffid,))	
			db.commit()

		elif ch == 2:
			newadd = raw_input("Enter the new address")
			cursor.execute("""UPDATE STAFF SET ADDRESS = %s WHERE STAFF_ID = %s;""", (newadd, staffid,))	
			db.commit()

		elif ch == 3:
			oldnumber = raw_input("Enter the old number")
			newnumber = raw_input("Enter the new number")
			cursor.execute("""UPDATE STAFF_CONTACT SET CONTACT_NUMBER = %s WHERE STAFF_ID = %s AND CONTACT_NUMBER = %s;""", (newnumber, staffid, oldnumber,))	
			db.commit()

		elif ch == 4:
			newsal = int(raw_input("Enter the new salary"))
			cursor.execute("""UPDATE SALARY SET BASE_SALARY = %s WHERE STAFF_ID = %s;""", (newsal, staffid,))	
			db.commit()

		elif ch == 5:
			newbon = int(raw_input("Enter the new bonus to replace existing bonus"))
			cursor.execute("""UPDATE SALARY SET BONUS = %s WHERE STAFF_ID = %s;""", (newbon, staffid,))	
			db.commit()

		elif ch == 6:
			newdeduc = int(raw_input("Enter the new deduction to replace existing deduction"))
			cursor.execute("""UPDATE SALARY SET DEDUCTIONS = %s WHERE STAFF_ID = %s;""", (newdeduc, staffid,))	
			db.commit()
		print("Details Updated!!")
	except:
		print("Error!")
		db.rollback()


while True:
	# Staff related functions
	print
	print("1: Add new Staff")
	print("2: Delete a Staff")
	print("3: Add Staff-Dependent Details")
	print("4: Set Manager for staff")
	print("5: Calculate Salary of Emloyee")
	print("6: Update Staff details")
	print
	#Customer related functions
	print("7: Add new customer")
	print("8: Update customer details")
	print
	#Food item related function
	print("9: Add new menu item")
	print("10: Change Price of Food Item")
	print("11: Show Most Ordered Item")
	print("12: Search Food item by name")
	print("13: Search Food item by category")
	print("14: Rate Food Item")
	print("15: See Average Rating of Food Item")
	print("16: Delete Food Item")
	print
	#order related function
	print("17: Place Order")
	print("18: Make Payment")
	print("19: Generate E-Invoice")
	print("0: Exit")
	print
	choice = int(input("Enter your choice: "))

	if choice == 1:
		addStaff()
	
	elif choice == 2:
		deleteStaff()

	elif choice == 3:
		addStaffDependent()

	elif choice == 4:
		setManager()

	elif choice == 5:
		calcSalary()

	elif choice == 6:
		editStaffDetails()

	elif choice == 7:
		addCustomer()

	elif choice == 8:
		updateCustomer()

	elif choice == 9:
		addMenu()

	elif choice == 10:
		changePrice()

	elif choice == 11:
		showMostOrdered()

	elif choice == 12:
		searchFoodByName()

	elif choice == 13:
		searchFoodByCategory()

	elif choice == 14:
		rateOrder2()

	elif choice == 15:
		calcAvgRating()

	elif choice == 17:
		placeOrder()	

	elif choice == 18:
		makePayment()

	elif choice == 16:
		deleteMenu()

	elif choice == 19:
		generateEInvoice()

	elif choice == 0:
		break

	else:
		print ("Enter a valid choice!!!")

	print ("\n------------------------------------------------------------------------\n")

cursor.close()
db.close()
print ('Hasta la\'vista')