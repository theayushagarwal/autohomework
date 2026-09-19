monthly_salary = 75000
rent_paid = 4200
eligible_hra = 0.06 * monthly_salary
print(f"Salary: {monthly_salary}, Rent: {rent_paid}, HRA Limit (6%): {eligible_hra}")
if rent_paid <= eligible_hra:
    print("Rent allowance matched")
else:
    print("Rent allowance not matched")
