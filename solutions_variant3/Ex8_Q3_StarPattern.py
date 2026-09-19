max_level = 4
for level in range(1, max_level + 1):
    leading_spaces = " " * (max_level - level)
    stars = "*" * (2 * level - 1)
    print(f"{leading_spaces}{stars}")
