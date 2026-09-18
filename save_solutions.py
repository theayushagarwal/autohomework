import os
from pathlib import Path

SOLUTIONS = {
    "Ex2_Datatypes": '''# Exercise 2: Basic Datatypes & Predict the Output

# Predict the Output
x = 25
print("x = 25, type:", type(x))

x = 25.0
print("x = 25.0, type:", type(x))

x = 100
x = "VIT"
print("x = 'VIT', type:", type(x))

a = "Python"
print("a:", a)

x = 2 + 5j
print("x = 2+5j, type:", type(x))

print("Hello\\nPython")
print("Name\\tAge")
print("VIT\\\\Python")
print('He said "Hello!"')
print("It's Python")

# Corrected errors
name = "Rahul"
city = "Chennai"
age = 18
print("Name:", name)
print("City:", city)
print("Age:", age)
print("Hello")
x = 3 + 4j
print("Complex:", x)

# Hello World
print("Hello World")
''',

    "Ex3_Q1_Chars": '''# Exercise 3 - Q1: First, Fifth, and Last character of "Python Programming"
s = "Python Programming"
print("String:", s)
print("First character :", s[0])
print("Fifth character :", s[4])
print("Last character  :", s[-1])
''',

    "Ex3_Q2_Slicing": '''# Exercise 3 - Q2: Slicing "Python Programming"
s = "Python Programming"
print("Original String:", s)
print("1. Python      :", s[0:6])
print("2. Programming :", s[7:18])
print("3. gram        :", s[10:14])
print("4. Pro         :", s[7:10])
print("5. ming        :", s[14:18])
''',

    "Ex3_Q3_NegIndex": '''# Exercise 3 - Q3: Negative indexing on "Vellore"
s = "Vellore"
print("String:", s)
print("Last character        :", s[-1])
print("Second last character :", s[-2])
print("Third last character  :", s[-3])
''',

    "Ex3_Q4_PrintA": '''# Exercise 3 - Q4: Without typing the letter A anywhere in the program, print A
print(chr(65))
''',

    "Ex3_Q5_ASCII": '''# Exercise 3 - Q5: Print the ASCII (Unicode) value of: A, a, Z, 0, @
chars = ['A', 'a', 'Z', '0', '@']
for c in chars:
    print(f"ASCII value of '{c}' is {ord(c)}")
''',

    "Ex3_Q6_Chr": '''# Exercise 3 - Q6: Print characters corresponding to: 65, 97, 48, 36, 90
codes = [65, 97, 48, 36, 90]
for code in codes:
    print(f"Character for {code} is '{chr(code)}'")
''',

    "Ex4_Q1_BioCard": '''# Exercise 4 - Q1: Student Bio Card
name = "Rahul"
age = 19
department = "CSE"
university = "VIT"
mobile = "9876543210"

print("*" * 35)
print("          STUDENT BIO CARD         ")
print("*" * 35)
print(f"Name       : {name}")
print(f"Age        : {age}")
print(f"Department : {department}")
print(f"University : {university}")
print(f"Mobile     : {mobile}")
print("*" * 35)
''',

    "Ex4_Q2_SingleAssign": '''# Exercise 4 - Q2: Assign name, age, and CGPA using a single assignment statement
name, age, cgpa = "Ayush", 19, 8.85
print("Name:", name)
print("Age :", age)
print("CGPA:", cgpa)
''',

    "Ex4_Q3_UnicodeChar": '''# Exercise 4 - Q3: Read a single character and display its Unicode value
ch = 'K'
print("Character:", ch)
print(f"Unicode value of '{ch}':", ord(ch))
''',

    "Ex4_Q4_StringIndex": '''# Exercise 4 - Q4: String character indexing
s = "ComputerScience"
print("String:", s)
print("First character       :", s[0])
print("Last character        :", s[-1])
print("Second character      :", s[1])
print("Second last character :", s[-2])
''',

    "Ex5_Q1_Supermarket": '''# Exercise 5 - Q1: Supermarket Bill & Arithmetic Operations
p1 = 120.50
p2 = 45.25
print(f"Price 1: {p1}, Price 2: {p2}")
print("Total price            :", p1 + p2)
print("Price difference       :", p1 - p2)
print("Product of prices      :", p1 * p2)
print("Division (p1 / p2)     :", p1 / p2)
print("Remainder (p1 % p2)    :", p1 % p2)
print("Floor division (p1//p2):", p1 // p2)
''',

    "Ex5_Q2_Relational": '''# Exercise 5 - Q2: Relational operations on student marks
marks_A = 85
marks_B = 92
print(f"Marks A: {marks_A}, Marks B: {marks_B}")
print("A == B :", marks_A == marks_B)
print("A != B :", marks_A != marks_B)
print("A > B  :", marks_A > marks_B)
print("A < B  :", marks_A < marks_B)
print("A >= B :", marks_A >= marks_B)
print("A <= B :", marks_A <= marks_B)
''',

    "Ex5_Q3_Bitwise": '''# Exercise 5 - Q3: Bitwise operations on permission codes
code1 = 12
code2 = 25
print(f"Code 1: {code1} (Binary: {bin(code1)})")
print(f"Code 2: {code2} (Binary: {bin(code2)})")
print(f"Bitwise AND       : {code1 & code2} ({bin(code1 & code2)})")
print(f"Bitwise OR        : {code1 | code2} ({bin(code1 | code2)})")
print(f"Bitwise XOR       : {code1 ^ code2} ({bin(code1 ^ code2)})")
print(f"Complement (Code1): {~code1} ({bin(~code1)})")
print(f"Left Shift  (<< 1): {code1 << 1} ({bin(code1 << 1)})")
print(f"Right Shift (>> 1): {code1 >> 1} ({bin(code1 >> 1)})")
''',

    "Ex5_Q4_Precedence": '''# Exercise 5 - Q4: Operator Precedence
print("5 + 3 * 2   =", 5 + 3 * 2)
print("(5 + 3) * 2 =", (5 + 3) * 2)
print("2 ** 3 * 2  =", 2 ** 3 * 2)
print("2 ** 3 ** 2 =", 2 ** 3 ** 2)
''',

    "Ex6_Q1_Attendance": '''# Exercise 6 - Q1: Attendance Check
attendance = 82
print(f"Attendance percentage: {attendance}%")
if attendance >= 75:
    print("Student is permitted")
else:
    print("Student not permitted")
''',

    "Ex6_Q2_Multiple": '''# Exercise 6 - Q2: Multiple of 2 or 5
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
''',

    "Ex6_Q3_Greatest": '''# Exercise 6 - Q3: Greatest of three numbers
a, b, c = 45, 89, 23
print(f"Numbers: a={a}, b={b}, c={c}")
if a >= b and a >= c:
    print(f"Greatest is a: {a}")
elif b >= a and b >= c:
    print(f"Greatest is b: {b}")
else:
    print(f"Greatest is c: {c}")
''',

    "Ex6_Q4_Grades": '''# Exercise 6 - Q4: Grade Scoring
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
''',

    "Ex6_Q5_Rent": '''# Exercise 6 - Q5: House rent allowance
salary = 50000
rent = 2800
allowance = 0.06 * salary
print(f"Salary: {salary}, House Rent: {rent}, 6% Allowance: {allowance}")
if rent <= allowance:
    print("Rent allowance matched")
else:
    print("Rent allowance not matched")
''',

    "Ex7_Q1_Factorial": '''# Exercise 7 - Q1: Factorial using while loop
n = 5
fact = 1
i = 1
while i <= n:
    fact *= i
    i += 1
print(f"Factorial of {n} is: {fact}")
''',

    "Ex7_Q2_Table": '''# Exercise 7 - Q2: Multiplication table using while loop
n = 7
print(f"Multiplication Table for {n}:")
i = 1
while i <= 10:
    print(f"{n} x {i} = {n * i}")
    i += 1
''',

    "Ex7_Q3_ReverseDigits": '''# Exercise 7 - Q3: Reverse digits using while loop (arithmetic only)
num = 12345
print("Original number:", num)
rev = 0
temp = num
while temp > 0:
    digit = temp % 10
    rev = (rev * 10) + digit
    temp = temp // 10
print("Reversed number:", rev)
''',

    "Ex8_Q1_Denomination": '''# Exercise 8 - Q1: Currency Denomination
amount = 3885
print("Amount:", amount)
notes = [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1]
remaining = amount
print("Denominations:")
for note in notes:
    if remaining >= note:
        count = remaining // note
        remaining = remaining % note
        print(f"Rs. {note} x {count}")
''',

    "Ex8_Q2_Patterns": '''# Exercise 8 - Q2: Number pattern and star pyramid pattern
print("--- Number Pattern ---")
for i in range(5, 0, -1):
    for j in range(i, 0, -1):
        print(j, end=" ")
    print()

print("\\n--- Star Pyramid Pattern ---")
rows = 4
for i in range(1, rows + 1):
    print(" " * (rows - i) + "*" * (2 * i - 1))
'''
}

out_dir = Path(r"c:\Users\ayush\Downloads\files (2)\solutions")
out_dir.mkdir(exist_ok=True)
for q_id, code in SOLUTIONS.items():
    p = out_dir / f"{q_id}.py"
    p.write_text(code, encoding="utf-8")
    print(f"Saved: {p.name}")
