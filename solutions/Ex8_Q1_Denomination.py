amount = 3885
print("Amount:", amount)
notes = [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1]
remaining = amount
print("Denominations:")
for note in notes:
    if remaining >= note:
        count = remaining // note
        remaining = remaining % note
        print(f"Rs. {note} x {count}")
