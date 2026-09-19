amount = int(input())
print("Denomination breakdown:")
notes = [2000, 500, 100, 50, 20, 10, 5, 2, 1]
for n in notes:
    while amount >= n:
        print("Rs.", n)
        amount -= n
