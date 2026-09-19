lines = 5
row = lines
while row >= 1:
    col = row
    while col >= 1:
        print(col, end="\t")
        col -= 1
    print()
    row -= 1
