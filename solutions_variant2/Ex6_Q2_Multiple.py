a = int(input())
if (a % 2 == 0 and a % 5 == 0):
    print("Num is multiple of 2 and 5")
elif a % 2 == 0:
    print("Num is multiple of 2")
elif a % 5 == 0:
    print("Num is multiple of 5")
else:
    print("Num is neither multiple of 2 nor 5")
