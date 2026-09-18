salary = 50000
rent = 2800
allowance = 0.06 * salary
print(f"Salary: {salary}, House Rent: {rent}, 6% Allowance: {allowance}")
if rent <= allowance:
    print("Rent allowance matched")
else:
    print("Rent allowance not matched")
