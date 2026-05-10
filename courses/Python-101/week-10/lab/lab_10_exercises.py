# lab_10_exercises.py
# Python 101 — Week 10: Modules & Packages
# Fitzwilliam Institute

import math
import random
import os
import json
from datetime import datetime, date, timedelta

# ── Exercise 1 ────────────────────────────────────────────────
# Use the math module to:
#   a) Print pi to 5 decimal places
#   b) Calculate the hypotenuse of a right triangle with sides 3 and 4
#   c) Round 7.6 DOWN to the nearest integer (use math.floor)
#   d) Round 7.2 UP to the nearest integer (use math.ceil)


# ── Exercise 2 ────────────────────────────────────────────────
# Use the random module to:
#   a) Generate 5 random integers between 1 and 100
#   b) Pick a random item from the list below
#   c) Shuffle the list in-place and print it
items = ["apple", "banana", "cherry", "date", "elderberry"]


# ── Exercise 3 ────────────────────────────────────────────────
# Use the datetime module to:
#   a) Print today's date
#   b) Calculate what date it will be 100 days from today
#   c) Calculate how many days until New Year's Day next year


# ── Exercise 4 ────────────────────────────────────────────────
# Use the os module to:
#   a) Print the current working directory
#   b) List all files in the current directory
#   c) Check if a file called "students.csv" exists in the week-08/lab folder
#      (Tip: use os.path.join and os.path.exists)


# ── Exercise 5 ────────────────────────────────────────────────
# A student record is stored as a Python dictionary.
# a) Convert it to a JSON string using json.dumps() (indent=2 for pretty print)
# b) Save the JSON to a file called "student.json"
# c) Read the file back and load it as a Python dict using json.loads()
# d) Print the student's name from the loaded dict
student = {
    "name": "Alice",
    "age": 21,
    "courses": ["Python 101", "Web Dev"],
    "scores": {"Python 101": 88, "Web Dev": 74},
}


# ── Exercise 6 (Stretch) ──────────────────────────────────────
# Generate a "lucky numbers" ticket:
#   - 6 unique random integers between 1 and 50
#   - 1 "bonus ball" between 1 and 20
# Sort the main numbers and print the ticket nicely.
# Example: "Lucky numbers: 3 11 18 27 34 41 | Bonus: 7"
