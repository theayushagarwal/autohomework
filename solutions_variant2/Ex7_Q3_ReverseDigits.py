original = 98765
print("Input number:", original)
reversed_val = 0
n = original
while n > 0:
    rem = n % 10
    reversed_val = reversed_val * 10 + rem
    n //= 10
print("Reversed number:", reversed_val)
