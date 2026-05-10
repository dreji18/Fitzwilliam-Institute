# lab_03_solutions.py
# Python 101 — Week 03 — SOLUTIONS
# ⚠️  STAFF ONLY

# Exercise 1
temperature = 24
if temperature < 10:
    print("Cold")
elif temperature <= 20:
    print("Mild")
elif temperature <= 30:
    print("Warm")
else:
    print("Hot")

# Exercise 2
age = 17
has_student_card = True
if age < 12:
    price = 5
elif has_student_card:
    price = 8
else:
    price = 12
print(f"Ticket price: €{price}")

# Exercise 3
year = 2024
if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(f"{year} is a leap year")
else:
    print(f"{year} is not a leap year")

# Exercise 4
password = "SecurePass1"
long_enough  = len(password) >= 8
has_digit    = any(c.isdigit() for c in password)
has_upper    = any(c.isupper() for c in password)
if long_enough and has_digit and has_upper:
    print("Strong password")
else:
    print("Weak password")

# Exercise 5
score = 73
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
print(f"Score {score} → Grade {grade}")

# Exercise 6 (Stretch)
for n in [15, 9, 20, 7]:
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)
