a, b, c = 45, 89, 23
print(f"Numbers: a={a}, b={b}, c={c}")
if a >= b and a >= c:
    print(f"Greatest is a: {a}")
elif b >= a and b >= c:
    print(f"Greatest is b: {b}")
else:
    print(f"Greatest is c: {c}")
