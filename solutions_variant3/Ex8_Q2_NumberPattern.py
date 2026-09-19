limit = 5
for row in range(limit, 0, -1):
    for col in range(row, 0, -1):
        print(col, end="\t")
    print()
