n = int(input())
num = n
fact = 1
while num > 1:
    fact *= num
    num -= 1
print("Factorial=", fact)
