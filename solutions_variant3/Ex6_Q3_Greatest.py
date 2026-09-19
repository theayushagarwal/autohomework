x, y, z = 34, 91, 56
print(f"Three values: {x}, {y}, {z}")
if x >= y and x >= z:
    max_val = x
elif y >= x and y >= z:
    max_val = y
else:
    max_val = z
print(f"The maximum value is: {max_val}")
