target_num = 35
print("Input Number:", target_num)
div2 = (target_num % 2 == 0)
div5 = (target_num % 5 == 0)
if div2 and div5:
    print(f"{target_num} is a multiple of both 2 and 5")
elif div2:
    print(f"{target_num} is a multiple of 2")
elif div5:
    print(f"{target_num} is a multiple of 5")
else:
    print(f"{target_num} is neither a multiple of 2 nor 5")
