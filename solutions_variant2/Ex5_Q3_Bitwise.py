c1 = int(input())
c2 = int(input())
print("Binary of code1:", bin(c1))
print("Binary of code2:", bin(c2))
AND = c1 & c2
print("Bitwise AND:")
print("Decimal:", AND)
print("Binary:", bin(AND))
OR = c1 | c2
print("Bitwise OR:")
print("Decimal:", OR)
print("Binary:", bin(OR))
XOR = c1 ^ c2
print("Bitwise XOR:")
print("Decimal:", XOR)
print("Binary:", bin(XOR))
COMPLIMENT = ~c1
print("Bitwise compliment of code1:")
print("Decimal:", COMPLIMENT)
print("Binary:", bin(COMPLIMENT))
LEFT_SHIFT = c1 << 1
print("Left shift of code1 by 1:")
print("Decimal:", LEFT_SHIFT)
print("Binary:", bin(LEFT_SHIFT))
RIGHT_SHIFT = c1 >> 1
print("Right shift of code1 by 1:")
print("Decimal:", RIGHT_SHIFT)
print("Binary:", bin(RIGHT_SHIFT))
