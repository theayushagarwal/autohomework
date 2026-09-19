base_salary = 60000
house_rent = 3500
hra_limit = base_salary * 0.06
print("Salary:", base_salary, "| Rent:", house_rent, "| Allowed 6%:", hra_limit)
if house_rent <= hra_limit:
    print("Rent allowance matched")
else:
    print("Rent allowance not matched")
