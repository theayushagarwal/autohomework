cash = 5490
print("Total Amount:", cash)
denoms = [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1]
print("Denominations:")
for note in denoms:
    count = cash // note
    if count:
        print(f"Rs. {note:4d} : {count} note(s)")
        cash %= note
