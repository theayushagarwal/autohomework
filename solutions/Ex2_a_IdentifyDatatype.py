vals = [25, 25.0, "25", 'Python', True, False, 3+4j, -18, "True", 0.0, "3+4j", 0]
for v in vals:
    print(repr(v), ":", type(v).__name__)
