items = (25, 25.0, '25', 'Python', True, False, 3+4j, -18, 'True', 0.0, '3+4j', 0)
for element in items:
    print(f"{element} -> {type(element).__name__}")
