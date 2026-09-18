marks = 85
print("Marks:", marks)
if marks >= 91:
    grade = "S"
elif marks >= 81:
    grade = "A"
elif marks >= 71:
    grade = "B"
elif marks >= 61:
    grade = "C"
elif marks >= 51:
    grade = "D"
elif marks == 50:
    grade = "Pass"
else:
    grade = "Fail"
print("Grade:", grade)
