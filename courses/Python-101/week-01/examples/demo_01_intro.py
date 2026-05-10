# demo_01_intro.py
# Python 101 — Week 01 Live Demo
# Fitzwilliam Institute

# ── Output ──────────────────────────────────────────────────────
print("Python executes line by line, top to bottom.")
print("Each print() shows one line of output.")
print()  # blank line

# ── Variables ───────────────────────────────────────────────────
course   = "Python 101"
students = 25
rating   = 4.9
active   = True

print("Course:", course)
print("Students:", students)
print("Rating:", rating)
print("Active:", active)
print()

# ── Types ───────────────────────────────────────────────────────
print(type(course))    # <class 'str'>
print(type(students))  # <class 'int'>
print(type(rating))    # <class 'float'>
print(type(active))    # <class 'bool'>
print()

# ── Arithmetic ──────────────────────────────────────────────────
a, b = 17, 5
print("a + b  =", a + b)
print("a - b  =", a - b)
print("a * b  =", a * b)
print("a / b  =", a / b)    # float division
print("a // b =", a // b)   # floor division
print("a % b  =", a % b)    # modulo (remainder)
print("a ** b =", a ** b)   # exponentiation
