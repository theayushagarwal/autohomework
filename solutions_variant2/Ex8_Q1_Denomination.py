total_cash = 4785
print("Given Amount:", total_cash)
denominations = (2000, 500, 200, 100, 50, 20, 10, 5, 2, 1)
curr = total_cash
print("Breakdown:")
for d in denominations:
    qty = curr // d
    if qty > 0:
        print(f"Rs {d}: {qty} note(s)")
        curr %= d
