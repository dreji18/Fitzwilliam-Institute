# demo_01_intro.py
# Python 101 — Week 01: Live Demo
# Fitzwilliam Institute
#
# This file contains the code demonstrated during the lecture.
# Students can run it and experiment with it freely.

# ── Running Python ──────────────────────────────────────────
# Python executes top-to-bottom, line by line.
print("Python runs from top to bottom.")
print("Each print() call produces one line of output.")

# ── Variables ───────────────────────────────────────────────
# A variable stores a value. You choose the name.
course = "Python 101"
students = 20
print("Course:", course)
print("Students:", students)

# ── Data types ──────────────────────────────────────────────
# str  → text, wrapped in quotes
# int  → whole number
# float → decimal number
# bool → True or False

name   = "Fitzwilliam"   # str
year   = 2024            # int
price  = 9.99            # float
active = True            # bool

print(type(name), type(year), type(price), type(active))

# ── Arithmetic ──────────────────────────────────────────────
a = 10
b = 3

print("Addition:      ", a + b)
print("Subtraction:   ", a - b)
print("Multiplication:", a * b)
print("Division:      ", a / b)   # always returns float
print("Integer div:   ", a // b)  # floor division
print("Remainder:     ", a % b)   # modulo
print("Power:         ", a ** b)  # exponent

# ── String basics ───────────────────────────────────────────
greeting = "Hello"
audience = "class"
print(greeting + ", " + audience + "!")  # concatenation
print(f"{greeting}, {audience}!")        # f-string (preferred)
