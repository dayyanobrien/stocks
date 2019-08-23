import math
import sqlite3
import re

totalprice = 0 #Sets the total price of the receipt to 0 since nothing has been bought yet

db = sqlite3.connect(':memory:')
db = sqlite3.connect('shop.sqlite3') #Creates a database named shop
cursor = db.cursor()#Sets cursor for changing and creating tables around

cursor.execute('''DROP TABLE IF EXISTS receipt''') #Clears receipt

cursor.execute('''CREATE TABLE IF NOT EXISTS shop
    (GTIN8 TEXT PRIMARY KEY unique, Product TEXT unique, Price INTEGER, Stock INTEGER) ''') #Creates table shop
cursor.execute('''CREATE TABLE IF NOT EXISTS receipt 
    (GTIN8 TEXT PRIMARY KEY unique, Product TEXT unique, Price INTEGER, Quantity INTEGER, Total INTEGER) ''') #Creates table receipt

#To do:
#Finish adding comments to lines of importance
#Fix any bugs that I recieve from destructive testing. Currently unicode and add symbol check for add_a_product()


#---------------------------------------------------------------  INTRO

def intro():
    print("\n" + "Which would you like to do?")
    print("A: GTIN-8 code creator [Task 1 (i)]")
    print("B: GTIN-8 code validation [Task 1 (ii)]")
    print("C: Product store [Task 2]")
    print("D: Refill [Task 3]")
    print("E: Quit")
    what_do_you_want = input(str("A, B, C, D or E? "))
    if what_do_you_want == 'A' or what_do_you_want == 'a':
        creator()
    elif what_do_you_want == 'B' or what_do_you_want == 'b':
        validation()
    elif what_do_you_want == 'C' or what_do_you_want == 'c':
        store()
    elif what_do_you_want == 'D' or what_do_you_want == 'd':
        refill()
    elif what_do_you_want == 'E' or what_do_you_want == 'e':
        quit()
    else:
       print("ERROR: Invalid.")
       intro()

#---------------------------------------------------------------  TASK 1 (i)        

def creator():
    print('\n' + 'What would you like to do?')
    print('A: Find the 8th digit of your GTIN-8 code')
    print('B: Quit to main menu')
    print('C: Quit the program')
    which_one = input('A, B or C? ')
    if which_one == 'A' or which_one == 'a':
        GTIN_8_creator()
    elif which_one == 'B' or which_one == 'b':
        intro()
    elif which_one == 'C' or which_one == 'c':
        f = open("Receipt.txt", 'w').close()
        quit()
    else:
        print("ERROR: Invalid.")
        creator()

def GTIN_8_creator():
    everything = input("\n" + "Input your 7 digit GTIN-8 code: ")
    everything_str=str(everything)
    if len(everything_str) == 7:
        print("Length of GTIN-8 code is real.")
        if everything.isdigit() == True:
            print("GTIN-8 code is a digit.")
            ThreeAndOne = (int(everything_str[0]) * 3 + int(everything_str[1]) + int(everything_str[2]) * 3 + int(everything_str[3]) + int(everything_str[4]) * 3 + int(everything_str[5]) + int(everything_str[6]) * 3)
            HighestTen = int(math.ceil(ThreeAndOne / 10.0)) * 10
            number8 = HighestTen - ThreeAndOne
            print("The eighth digit is {}.".format(number8))
            creator()
        else:
            print("ERROR: GTIN-8 code is not a digit.")
            creator()
    else:
        print("ERROR: Length of GTIN-8 code is fake.")
        creator()

#---------------------------------------------------------------  TASK 1 (ii)       

def validation():
    print('\n' + 'What would you like to do?')
    print('A: Validate your GTIN-8 code')
    print('B: Quit to main menu')
    print('C: Quit the program')
    what = input('A, B or C? ')
    if what == 'A' or what == 'a':
        GTIN_8_validator()
    elif what == 'B' or what == 'b':
        intro()
    elif what == 'C' or what == 'c':
        f = open("Receipt.txt", 'w').close()
        quit()
    else:
        print("ERROR: Invalid.")
        validation()


def GTIN_8_validator():
    everything = input("\n" + "Input your 8 digit GTIN-8 code: ")
    everything_str=str(everything)
    if len(everything_str) == 8:
        print("Length of GTIN-8 code is real.")
        if everything.isdigit() == True:
            print("GTIN-8 code is a digit.")
            ThreeAndOne = (int(everything_str[0]) * 3 + int(everything_str[1]) + int(everything_str[2]) * 3 + int(everything_str[3]) + int(everything_str[4]) * 3 + int(everything_str[5]) + int(everything_str[6]) * 3)
            HighestTen = int(math.ceil(ThreeAndOne / 10.0)) * 10
            number8 = (HighestTen - ThreeAndOne)
            print("The eighth digit is {}.".format(number8))
            if number8 == int(everything_str[7]):
                print("Your GTIN-8 code is real.")
                validation()
            else:
                print("ERROR: Your GTIN-8 code is fake.")
                validation()
        else:
            print("ERROR: GTIN-8 code is not a digit.")
            validation()
    else:
        print("ERROR: Length of GTIN-8 code is fake.")
        validation()

#---------------------------------------------------------------  Task 2       

def store():
    print('\n' + 'What would you like to do?')
    print("A: Add a product to our store")
    print("B: List all products")
    print("C: Make your shopping list by barcode")
    print("D: Make your shopping list from name")
    print("E: View your shopping list")
    print("F: Quit to main menu")
    print("G: Quit program")
    A_or_B = input("A, B, C, D, E, F or G? ")
    if A_or_B == 'A' or A_or_B == 'a':
        add_a_product()
    elif A_or_B == 'B' or A_or_B == 'b':
        product_list()
    elif A_or_B == 'C' or A_or_B == 'c':
        barcode()
    elif A_or_B == 'D' or A_or_B == 'd':
        by_name()
    elif A_or_B == 'E' or A_or_B == 'e':
        receipt()
    elif A_or_B == 'F' or A_or_B == 'f':
        intro()
    elif A_or_B == 'G' or A_or_B == 'g':
        quit()
    else:
       print("ERROR: Invalid.")
       store()

def receipt():
    print("\n" + "Reading List...")
    cursor.execute("""SELECT total, (SELECT sum(total) FROM receipt) total FROM receipt""", )
    try:
        with db:
            totalprice = cursor.fetchone()[1]
            cursor.execute("""SELECT * FROM receipt""") #Selects everything from receipt
            rows = cursor.fetchall() #Set's all of the rows to row
            print(" GTIN-8      Product   Price(£) Quantity Total")
            for row in rows:
                print(row) #Prints every row on a seperate line

            print("Total Price: £" + str(totalprice)) #Prints the total price of everything
    except TypeError:
        print("ERROR: Nothing found in receipt.")
    finally:
        store()

def by_name():
    product_choice = input("\n" + 'What product do you want? ')
    if len(product_choice) <= 20:
        product_quantity = input("How many do you want? ")
        if product_quantity.isdigit() == True:
            if int(product_quantity) <= 50000:
                try:
                    with db:
                        cursor.execute("""SELECT Stock, Product FROM shop
                            WHERE Product = ?""", (product_choice,)) #Selects stocks and products from shop table
                        oldstock = cursor.fetchone()
                        oldstock, product = oldstock #Sets the old stock value to old stock
                        newstock = int(oldstock) - int(product_quantity) #Take the amount bought from the old stock to get the new stock
                        if newstock >= 0: #If this newstock is a negative, and therefore impossible it wont go through
                            cursor.execute("""SELECT Price,GTIN8 FROM shop
                                WHERE Product = ?""", (product_choice,))
                            price = cursor.fetchone()
                            price, product = price
                            try:
                                with db:
                                    cursor.execute("""SELECT Product, Price, GTIN8 FROM shop WHERE Product = ?""", (product_choice,)) #Selects data about product bought and puts it into receipt
                                    new = cursor.fetchone()
                                    cursor.execute("""INSERT INTO receipt(product, price, gtin8)
                                    VALUES(?,?,?)""", new)       
                            except sqlite3.IntegrityError: # Checks if the product inputted is unique
                                cursor.execute("""SELECT Price, Quantity FROM receipt WHERE Product = ?""", (product_choice,))
                                both = cursor.fetchone()
                                newprice, newquantity = both
                                product_quantity = int(product_quantity) + int(newquantity)
                            finally:
                                total = int(product_quantity)*float(price)
                                global totalprice
                                totalprice = totalprice + total #Adds amount bought to the total price
                                cursor.execute("""UPDATE receipt SET Quantity = ?, Total = ?
                                    WHERE Product = ? """, (product_quantity, total, product_choice,))
                                cursor.execute("""UPDATE shop SET Stock = ?
                                    WHERE Product = ? """, (newstock, product_choice,))
                                anything_else = input("Type y if you want anything else: ")
                                if anything_else == 'Y' or anything_else == 'y':
                                    db.commit()
                                    print('Data inserted.')
                                    by_name()
                                else:
                                    db.commit()
                                    print('Data inserted.')
                                    store()
                        else:
                            print("ERROR: Not enough stock available.")
                            store()
                except TypeError:
                    print("ERROR: Product doesn't exist/multiple products contain that string.")
                    store()
            else:
                print("ERROR: Product quantity too large.")
                store()
        else:
            print("ERROR: Product quantity is not a digit.")
            store()
    else:
        print("ERROR: Product name too large.")
        store()
               
def barcode():   
    product_choice = input("\n" + "Please write the GTIN-8 code of what you want: ")
    if len(product_choice) == 8:
        if product_choice.isdigit() == True:
            ThreeAndOne = (int(product_choice[0]) * 3 + int(product_choice[1]) + int(product_choice[2]) * 3 + int(product_choice[3]) + int(product_choice[4]) * 3 + int(product_choice[5]) + int(product_choice[6]) * 3)
            HighestTen = int(math.ceil(ThreeAndOne / 10.0)) * 10
            number8 = (HighestTen - ThreeAndOne)
            if number8 == int(product_choice[7]):
                product_quantity = input("How many do you want? ")
                if product_quantity.isdigit() == True:
                    if int(product_quantity) <= 50000:
                        try:
                            with db:
                                cursor.execute("""SELECT Stock, Product FROM shop WHERE GTIN8 = ?""", (product_choice,)) #Selects stocks and products from shop table
                                oldstock = cursor.fetchone()
                                oldstock, product = oldstock #Sets the old stock value to old stock
                                newstock = int(oldstock) - int(product_quantity) #Take the amount bought from the old stock to get the new stock
                                if newstock >= 0: #If this newstock is a negative, and therefore impossible it wont go through
                                    cursor.execute("""SELECT Price,GTIN8 FROM shop
                                        WHERE GTIN8 = ?""", (product_choice,))
                                    price = cursor.fetchone()
                                    price, product = price
                                    try:
                                        with db:
                                            cursor.execute("""SELECT Product, Price, GTIN8 FROM shop WHERE GTIN8 = ?""", (product_choice,)) #Selects data about product bought and puts it into receipt
                                            new = cursor.fetchone()
                                            cursor.execute("""INSERT INTO receipt(product, price, gtin8)
                                                VALUES(?,?,?)""", new)       
                                    except sqlite3.IntegrityError: # Checks if the product inputted is unique, if not it just adds the new quantity and total price on.
                                        cursor.execute("""SELECT Price, Quantity FROM receipt WHERE GTIN8 = ?""", (product_choice,))
                                        both = cursor.fetchone()
                                        newprice, newquantity = both
                                        product_quantity = int(product_quantity) + int(newquantity)
                                    finally:
                                        total = int(product_quantity)*float(price)
                                        cursor.execute("""UPDATE receipt SET Quantity = ?, Total = ?
                                            WHERE GTIN8 = ? """, (product_quantity, total, product_choice,))
                                        cursor.execute("""UPDATE shop SET Stock = ?
                                            WHERE GTIN8 = ? """, (newstock, product_choice,))
                                        anything_else = input("Type y if you want anything else: ")
                                        if anything_else == 'Y' or anything_else == 'y':
                                            db.commit()
                                            print('Data inserted.')
                                            barcode()
                                        else:
                                            db.commit()
                                            print('Data inserted.')
                                            store()
                                else:
                                    print("ERROR: Not enough stock available.")
                                    store()
                        except TypeError:
                            print("ERROR: Product doesn't exist.")
                            store()
                    else:
                        print("ERROR: Product quantity too large.")
                        store()
                else:
                    print("ERROR: Product quantity is not a digit.")
                    store()
            else:
                print("ERROR: Last digit of GTIN-8 code is fake.")
                store()
        else:
            print("ERROR: GTIN-8 code is not a digit.")
            store()
    else:
        print("ERROR: Length of GTIN-8 code is fake.")
        store()
   
def add_a_product():
    print("\n" + "Add a product to our store.")
    product_name = input("Write down the name of the product: ")
    if len(product_name) <= 20:
        if re.match("^[a-zA-Z0-9_]*$", product_name):
            GTIN_code = input("Write down the GTIN-8 CODE of the product: ")
            product_choice = str(GTIN_code)
            if len(product_choice) == 8: #Checks if GTIN-8 code is 8 digits long
                if GTIN_code.isdigit() == True: #Checks if GTIN-8 code is a digit
                    ThreeAndOne = (int(product_choice[0]) * 3 + int(product_choice[1]) + int(product_choice[2]) * 3 + int(product_choice[3]) + int(product_choice[4]) * 3 + int(product_choice[5]) + int(product_choice[6]) * 3)
                    HighestTen = int(math.ceil(ThreeAndOne / 10.0)) * 10
                    number8 = (HighestTen - ThreeAndOne)
                    if number8 == int(product_choice[7]): #Checks if the last digit of the GTIN-8 is real
                        product_price = input("Write down the price of the product: £")            
                        try:
                            product_price2 = float(product_price)
                            try:
                                product_price2 = int(product_price)
                            except ValueError:
                                if len(product_price.rsplit('.')[-1]) > 2:
                                    print("ERROR: Format for price not correct.")
                                    store()
                            finally:
                                if float(product_price) <= 50000:
                                    amount = input("How many are you offering? ")
                                    if amount.isdigit() == True:
                                        if int(amount) <= 50000:
                                            try:
                                                with db:
                                                    cursor.execute('''INSERT INTO shop
                                                        (GTIN8, product, price, stock)
                                                        VALUES(?,?,?,?)''', (GTIN_code,product_name, product_price, amount)) #Inserts the product into the table
                                                    print('Data inserted.')
                                                    db.commit()
                                            except sqlite3.IntegrityError: # Checks if the product inputted is unique
                                                    print("Product already exists.")
                                            finally:
                                                store()
                                        else:
                                            print("ERROR: Amount offered is too large")
                                            store()
                                    else:
                                        print("ERROR: Amount offered is not a digit.")
                                        store()
                                else:
                                    print("ERROR: Product price is too large.")
                                    store()
                        except ValueError:
                            print("ERROR: Price given is not a digit.")
                            store()
                    else:
                        print("ERROR: Your GTIN-8 code is fake.")
                        store()
                else:
                    print("ERROR: GTIN-8 code is not a digit.")
                    store()   
            else:
                print("ERROR: Length of GTIN-8 code is fake.")
                store()
        else:
            print("ERROR: Product name contains symbol(s)")
            store()
    else:
        print("ERROR: Product name too large.")
        store()
            
def product_list():
    print("\n" + "Reading List...")
    cursor.execute("SELECT * FROM shop")
    rows = cursor.fetchall() #Selects all rows in shop
    print(" GTIN-8      Product   Price(£) Stock")
    for row in rows: #In every row, it prints the row and then a new line
        print(row) 
    store()

#---------------------------------------------------------------  Task 3               

def refill():
    print('\n' + 'What would you like to do?')
    print("A: Refill products")
    print("B: Quit to main menu")
    print("C: Quit program")
    ref_or_quit = input("A or B or C? ")
    if ref_or_quit == 'A' or ref_or_quit == 'a':
        refillstocks()
    elif ref_or_quit == 'B' or ref_or_quit == 'b':
        intro()
    elif ref_or_quit == 'C' or ref_or_quit == 'c':
        quit()
    else:
        print("ERROR: Invalid.")
        refill()

def refillstocks():
    refill_limit = input("\n" + "What do you want the refill limit to be? ")
    if refill_limit.isdigit() == True:
        refilled = input("How much do you want the stock to be refilled with? ")
        if refilled.isdigit() == True:
            if int(refill_limit) <= int(refilled):
                cursor.execute("""UPDATE shop SET Stock = ?
                    WHERE Stock < ?""", (refilled, refill_limit,))
                db.commit()
                print("Stocks refilled.")
                refill()
            else:
                print("ERROR: Refill limit is more than what you want it to be refilled with.")
                refill()
        else:
            print("ERROR: What you wanted the stock to be refilled with is not a digit.")
            refill()
    else:
        print("ERROR: Your refill limit is not a digit.")
        refill()
                                  
#---------------------------------------------------------------       

intro()
            
