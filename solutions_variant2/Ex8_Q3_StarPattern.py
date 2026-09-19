total_rows = 4
r = 1
while r <= total_rows:
    spaces = " " * (total_rows - r)
    stars = "*" * (2 * r - 1)
    print(spaces + stars)
    r += 1
