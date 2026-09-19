mark = int(input())
if mark >= 91:
    print("Grade:S")
elif mark >= 81:
    print("Grade:A")
elif mark >= 71:
    print("Grade:B")
elif mark >= 61:
    print("Grade:C")
elif mark > 50:
    print("Grade:D")
elif mark == 50:
    print("Pass")
else:
    print("Fail")
