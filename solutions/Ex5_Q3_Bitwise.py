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
