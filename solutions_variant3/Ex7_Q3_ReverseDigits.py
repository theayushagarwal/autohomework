val = 74628
print("Input integer:", val)
inverted = 0
while val > 0:
    inverted = (inverted * 10) + (val % 10)
    val //= 10
print("Reversed integer:", inverted)
