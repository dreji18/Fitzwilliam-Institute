# lab_02_exercises.py
# Python 101 — Week 02: Data Types & Strings
# Fitzwilliam Institute

# ── Exercise 1 ────────────────────────────────────────────────
# The variable below is a string, but we need it as an integer.
# Convert it and add 10 to it. Print the result.
age_str = "28"


# ── Exercise 2 ────────────────────────────────────────────────
# Create variables: name (str), age (int), height_m (float), is_student (bool)
# Use an f-string to print one sentence containing all four values.
# Example: "Alice is 22 years old, 1.72 m tall, and is a student: True"


# ── Exercise 3 ────────────────────────────────────────────────
# Given the sentence below, use string methods to:
#   a) Print it in ALL CAPS
#   b) Print it in all lowercase
#   c) Count how many times the letter 'e' appears (case-insensitive)
#   d) Replace "Python" with "coding"
sentence = "Python is easy to learn and fun to use."


# ── Exercise 4 ────────────────────────────────────────────────
# Given the messy string below:
#   a) Strip the whitespace from both ends
#   b) Check if it starts with "Hello"
#   c) Split it into a list of words and print the list
messy = "   Hello there, world!   "


# ── Exercise 5 ────────────────────────────────────────────────
# Format a price receipt using an f-string:
#   item = "Notebook"
#   price = 4.5
#   qty = 3
# Print: "3x Notebook @ €4.50 each = €13.50"
# Hint: use :.2f to format floats to 2 decimal places


# ── Exercise 6 (Stretch) ──────────────────────────────────────
# Without using len(), figure out if the string below is a palindrome
# (reads the same forwards and backwards). Print True or False.
# Hint: use string slicing [::-1]
word = "racecar"
