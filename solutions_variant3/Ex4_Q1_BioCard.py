student_record = {
    "Name": "Pooja Hegde",
    "Age": 19,
    "Department": "CSE Core",
    "University": "VIT",
    "Mobile": "9845123456"
}

print("-----------------------------------")
print("          BIO-DATA CARD            ")
print("-----------------------------------")
for k, v in student_record.items():
    print(f"{k:<12}: {v}")
print("-----------------------------------")
