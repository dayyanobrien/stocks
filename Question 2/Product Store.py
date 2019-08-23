import math
import sqlite3

total = 0 

def what_to_do():
    print("\n" + "Amazon")
    print("What would you like to do?")
    print("A: Add a product to our store")
    print("B: List all products")
    print("C: Make your shopping list by barcode")
    print("D: Make your shopping list from name")
    print("E: View your final shopping list")
    print("F: Quit & Clear Recipt")
    A_or_B = input("A, B, C, D, E or F? ")
    if A_or_B == 'A' or A_or_B == 'a':
        add_a_product()
    elif A_or_B == 'B' or A_or_B == 'b':
        product_list()
    elif A_or_B == 'C' or A_or_B == 'c':
        barcode()
    elif A_or_B == 'D' or A_or_B == 'd':
        by_name()
    elif A_or_B == 'E' or A_or_B == 'e':
        recipt()
    elif A_or_B == 'F' or A_or_B == 'f':
        f = open("Recipt.txt", 'w').close()
        quit()
    else:
       print("Invalid")
       what_to_do()

def recipt():
    f = open("Recipt.txt", 'r')
    lines = f.readlines()
    print("\n" + "Showing Recipt...")
    print(lines)
    print(len(lines))
    for line in lines:
        print(line)
    f.close()
    print("Total Price: £" + str(total))
    f = open('Recipt.txt', 'a')
    f.write("Total Price: £" + str(total))
    f.close()
    print("Please save to the recipt.txt file")
    bye = input("Please press any key to exit the program and clear your recipt: ")
    if bye == 'y':
        f = open('Recipt.txt', 'w').close()
        quit
    else:
        f = open('Recipt.txt', 'w').close()
        quit

def by_name():
    print("\n" + "Amazon")
    product_choice = input("Please write the name of what you want: ")
    product_quantity = int(input("How many do you want? "))
    f = open("Products.txt", 'r')
    lines = f.readlines()
    for i in range(0,len(lines)):
        line = lines[i]
        if product_choice in (line):
            f = open("Recipt.txt", 'a')
            f.write(lines[i])
            f.write(lines[i+1])
            f.write("Product Number: " + str(product_quantity) + "\n")
            f.write("\n")
            text = (lines[i+1])
            price = float(text.split("£")[1])
            amount = (product_quantity * price)
            global total
            total += amount
            anything_else = input("Type y if you want anything else: ")
            if anything_else == 'y':
                f.close()
                by_name()
            else:
                f.close()
                what_to_do()
            break
        
def barcode():   
    print("\n" + "Amazon")
    product_choice = input("Please write the GTIN-8 code of what you want: ")
    if len(product_choice) == 8:
        if product_choice.isdigit() == True:
            product_quantity = int(input("How many do you want? "))
            f = open("Products.txt", 'r')
            lines = f.readlines()
            for i in range(0,len(lines)):
                line = lines[i]
                if product_choice in (line):
                    f = open("Recipt.txt", 'a')
                    f.write(lines[i+1])
                    f.write(lines[i+2])
                    f.write("Product Number: " + str(product_quantity) + "\n")
                    f.write("\n")
                    text = (lines[i+2])
                    price = float(text.split("£")[1])
                    amount = (product_quantity * price)
                    global total
                    total += amount
                    anything_else = input("Type y if you want anything else: ")
                    if anything_else == 'y':
                        f.close()
                        barcode()
                    else:
                        f.close()
                        what_to_do()
                    break
        else:
            print("GTIN 8 code you inputted is not real")
            what_to_do()
    else:
        print("GTIN 8 code you inputted is not real")
        what_to_do()
   
def add_a_product():
    print("\n" + "Amazon")
    print("Add a product to our store")
    product_name = input("Write down the name of the product: ")
    GTIN_code = input("Write down the GTIN-8 CODE of the product: ")
    GTIN_code_str = str(GTIN_code)
    if len(GTIN_code_str) == 8:
        print("Length of GTIN-8 code is real")
        if GTIN_code.isdigit() == True:
            print("GTIN-8 code is a digit")
            ThreeAndOne = (int(GTIN_code_str[0]) * 3 + int(GTIN_code_str[1]) + int(GTIN_code_str[2]) * 3 + int(GTIN_code_str[3]) + int(GTIN_code_str[4]) * 3 + int(GTIN_code_str[5]) + int(GTIN_code_str[6]) * 3)
            HighestTen = int(math.ceil(ThreeAndOne / 10.0)) * 10
            number8 = (HighestTen - ThreeAndOne)
            print("The eighth digit is", + number8)
            if number8 == int(GTIN_code_str[7]):
                print("Your GTIN-8 code is real")
                GTIN_code_int = int(GTIN_code)
                product_price = input("Write down the price of the product: ")
                amount = input("How many are you offering? ")
                amount_int = int(amount)
                db = sqlite3.connect(':memory:')
                db = sqlite3.connect('shop.sqlite3')
                cursor = db.cursor()
                cursor.execute('''CREATE TABLE IF NOT EXISTS shop
                    (GTIN8 INTEGER PRIMARY KEY unique,
                    Product TEXT unique,
                    Price TEXT,
                    Stock INTEGER)
                    ''')
                cursor.execute('''INSERT INTO shop
                    (GTIN8, product, price, stock)
                    VALUES(?,?,?,?)''', (GTIN_code_int,product_name, product_price, amount_int))
                print('Data inserted')
                db.commit()
                db.close()
                what_to_do()
            else:
                print("Your GTIN-8 code is fake")
                what_to_do()
        else:
            print("GTIN-8 code is not a digit")
            what_to_do()   
    else:
        print("Length of GTIN-8 code is fake")
        what_to_do()
            
def product_list():
    f = open("Products.txt", 'r')
    lines = f.readlines()
    print("\n" + "Reading List...")
    print(lines)
    print(len(lines))
    for line in lines:
        print(line)
    f.close()
    what_to_do()

what_to_do()

      
      
      

