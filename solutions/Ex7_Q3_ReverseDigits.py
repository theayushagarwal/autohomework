num = 12345
print("Original number:", num)
rev = 0
temp = num
while temp > 0:
    digit = temp % 10
    rev = (rev * 10) + digit
    temp = temp // 10
print("Reversed number:", rev)
