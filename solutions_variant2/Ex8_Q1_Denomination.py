amount = int(input(""))
print("Denomination breakdown:")
while amount > 0:
    if amount >= 2000:
        print("Rs. 2000")
        amount = amount - 2000
    elif amount >= 500:
        print("Rs. 500")
        amount = amount - 500
    elif amount >= 100:
        print("Rs. 100")
        amount = amount - 100
    elif amount >= 50:
        print("Rs. 50")
        amount = amount - 50
    elif amount >= 20:
        print("Rs. 20")
        amount = amount - 20
    elif amount >= 10:
        print("Rs. 10")
        amount = amount - 10
    elif amount >= 5:
        print("Rs. 5")
        amount = amount - 5
    elif amount >= 2:
        print("Rs. 2")
        amount = amount - 2
    else:
        print("Rs. 1")
        amount = amount - 1
