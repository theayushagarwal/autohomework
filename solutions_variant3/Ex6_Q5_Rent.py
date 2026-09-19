salary = int(input())
rent = int(input())
allowance = 0.06 * salary
if rent <= allowance:
    print("Rent allowance matched")
else:
    print("Rent allowance not matched")
