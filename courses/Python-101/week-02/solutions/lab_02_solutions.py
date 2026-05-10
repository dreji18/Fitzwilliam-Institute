# lab_02_solutions.py
# Python 101 — Week 02: Variables, Types & Operators — SOLUTIONS
# Fitzwilliam Institute
#
# ⚠️  STAFF ONLY — Do not share with students before the lab is complete.

# ─────────────────────────────────────────────
# Exercise 1
# ─────────────────────────────────────────────
student_name = "Alice"
student_age  = 21
gpa          = 3.7
is_enrolled  = True

print("Name:", student_name)
print("Age:", student_age)
print("GPA:", gpa)
print("Enrolled:", is_enrolled)

# ─────────────────────────────────────────────
# Exercise 2
# ─────────────────────────────────────────────
print(type(student_name))
print(type(student_age))
print(type(gpa))
print(type(is_enrolled))

# ─────────────────────────────────────────────
# Exercise 3
# ─────────────────────────────────────────────
print(f"{student_name} is {student_age} years old and has a GPA of {gpa}.")

# ─────────────────────────────────────────────
# Exercise 4
# ─────────────────────────────────────────────
ticket_price = 12.50
group_size   = 7
total        = ticket_price * group_size
print(f"Total cost for {group_size} tickets: €{total:.2f}")

# ─────────────────────────────────────────────
# Exercise 5 (Stretch)
# ─────────────────────────────────────────────
celsius    = 100
fahrenheit = (celsius * 9 / 5) + 32
print(f"{celsius}°C = {fahrenheit}°F")
