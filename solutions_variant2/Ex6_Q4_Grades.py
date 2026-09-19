a = int(input())
if a >= 91:
    print("Grade:S")
elif (a > 80 and a < 91):
    print("Grade:A")
elif (a > 70 and a < 81):
    print("Grade:B")
elif (a > 60 and a < 71):
    print("Grade:C")
elif (a > 50 and a < 61):
    print("Grade:D")
elif a == 50:
    print("Pass")
else:
    print("Fail")
