# lab_03_exercises.py
# Python 101 — Week 03: Control Flow
# Fitzwilliam Institute

# ── Exercise 1 ────────────────────────────────────────────────
# Given a temperature in Celsius, print:
#   "Cold"    if below 10
#   "Mild"    if 10–20
#   "Warm"    if 21–30
#   "Hot"     if above 30
temperature = 24


# ── Exercise 2 ────────────────────────────────────────────────
# A cinema charges:
#   €5  for under-12s
#   €8  for students (12+, with student card)
#   €12 for adults
# Given: age = 17, has_student_card = True
# Calculate and print the correct ticket price.
age = 17
has_student_card = True


# ── Exercise 3 ────────────────────────────────────────────────
# Check if a year is a leap year.
# Rules: divisible by 4, EXCEPT centuries (div by 100),
#        UNLESS also divisible by 400.
# Test with: 2000, 1900, 2024, 2023
year = 2024


# ── Exercise 4 ────────────────────────────────────────────────
# A password is "strong" if it meets ALL of these:
#   - At least 8 characters long
#   - Contains at least one digit (hint: any(c.isdigit() for c in pwd))
#   - Contains at least one uppercase letter
# Print "Strong password" or "Weak password"
password = "SecurePass1"


# ── Exercise 5 ────────────────────────────────────────────────
# A grade classifier. Given a score (0-100), print the grade:
#   A: 90-100  |  B: 80-89  |  C: 70-79  |  D: 60-69  |  F: below 60
score = 73


# ── Exercise 6 (Stretch) ──────────────────────────────────────
# FizzBuzz classic: for a given number n, print:
#   "FizzBuzz" if divisible by both 3 and 5
#   "Fizz"     if divisible by 3 only
#   "Buzz"     if divisible by 5 only
#   The number itself otherwise
# Test with n = 15, 9, 20, 7
n = 15
