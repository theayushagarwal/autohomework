code1 = int(input())
code2 = int(input())
print("Binary of code1:", bin(code1))
print("Binary of code2:", bin(code2))
res_and = code1 & code2
print("Bitwise AND:")
print("Decimal:", res_and)
print("Binary:", bin(res_and))
res_or = code1 | code2
print("Bitwise OR:")
print("Decimal:", res_or)
print("Binary:", bin(res_or))
res_xor = code1 ^ code2
print("Bitwise XOR:")
print("Decimal:", res_xor)
print("Binary:", bin(res_xor))
comp = ~code1
print("Bitwise compliment of code1:")
print("Decimal:", comp)
print("Binary:", bin(comp))
ls = code1 << 1
print("Left shift of code1 by 1:")
print("Decimal:", ls)
print("Binary:", bin(ls))
rs = code1 >> 1
print("Right shift of code1 by 1:")
print("Decimal:", rs)
print("Binary:", bin(rs))
