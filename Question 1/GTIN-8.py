import math
print("Find the 8th digit of your GTIN-8 code.")
GTIN_8 = input("Input your 7 digit GTIN-8 code: ")
GTIN_8_str=str(GTIN_8)
ThreeAndOne = (int(GTIN_8_str[0]) * 3 + int(GTIN_8_str[1]) + int(GTIN_8_str[2]) * 3 + int(GTIN_8_str[3]) + int(GTIN_8_str[4]) * 3 + int(GTIN_8_str[5]) + int(GTIN_8_str[6]) * 3)
HighestTen = int(math.ceil(ThreeAndOne / 10.0)) * 10
number8 = HighestTen - ThreeAndOne
print("The eighth digit is {}.".format(number8))




