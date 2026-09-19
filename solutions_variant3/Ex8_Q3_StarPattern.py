total_rows = 4
for r in range(1, total_rows + 1):
    spaces = " " * (total_rows - r)
    stars = "*" * (2 * r - 1)
    print(spaces + stars)
