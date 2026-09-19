score = 76
print("Marks scored:", score)
if score >= 91:
    res = "S"
elif score >= 81:
    res = "A"
elif score >= 71:
    res = "B"
elif score >= 61:
    res = "C"
elif score >= 51:
    res = "D"
elif score == 50:
    res = "Pass"
else:
    res = "Fail"
print(f"Final Grade: {res}")
