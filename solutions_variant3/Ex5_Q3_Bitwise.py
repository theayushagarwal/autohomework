a, b = 14, 27
print(f"Binary of {a} is {bin(a)}, Binary of {b} is {bin(b)}")
print("a AND b :", a & b, "->", bin(a & b))
print("a OR b  :", a | b, "->", bin(a | b))
print("a XOR b :", a ^ b, "->", bin(a ^ b))
print("NOT a   :", ~a, "->", bin(~a))
print("a << 1  :", a << 1, "->", bin(a << 1))
print("a >> 1  :", a >> 1, "->", bin(a >> 1))
