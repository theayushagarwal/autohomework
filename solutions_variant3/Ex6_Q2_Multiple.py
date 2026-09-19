n = int(input())
if n % 10 == 0:
    print("Num is multiple of 2 and 5")
elif n % 2 == 0:
    print("Num is multiple of 2")
elif n % 5 == 0:
    print("Num is multiple of 5")
else:
    print("Num is neither multiple of 2 nor 5")
