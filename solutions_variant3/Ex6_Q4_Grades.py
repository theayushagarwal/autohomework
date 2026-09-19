marks_scored = 93
print("Student marks:", marks_scored)
if marks_scored >= 91:
    g = 'S'
elif marks_scored >= 81:
    g = 'A'
elif marks_scored >= 71:
    g = 'B'
elif marks_scored >= 61:
    g = 'C'
elif marks_scored >= 51:
    g = 'D'
elif marks_scored == 50:
    g = 'Pass'
else:
    g = 'Fail'
print("Secured Grade:", g)
