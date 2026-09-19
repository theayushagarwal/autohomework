val = 20
print("Evaluating number:", val)
m2 = (val % 2 == 0)
m5 = (val % 5 == 0)
if m2 and m5:
    print(val, "is a multiple of both 2 and 5")
elif m2:
    print(val, "is a multiple of 2")
elif m5:
    print(val, "is a multiple of 5")
else:
    print(val, "is neither a multiple of 2 nor 5")
