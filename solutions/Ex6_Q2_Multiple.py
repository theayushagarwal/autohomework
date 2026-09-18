num = 15
print("Number:", num)
if num % 2 == 0 and num % 5 == 0:
    print(f"{num} is a multiple of both 2 and 5")
elif num % 2 == 0:
    print(f"{num} is a multiple of 2")
elif num % 5 == 0:
    print(f"{num} is a multiple of 5")
else:
    print(f"{num} is neither a multiple of 2 nor 5")
