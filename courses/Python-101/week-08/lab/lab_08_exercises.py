# lab_08_exercises.py
# Python 101 — Week 08: File I/O
# Fitzwilliam Institute

import csv
import os

# ── Exercise 1 ────────────────────────────────────────────────
# Write a poem (at least 4 lines) to a file called "poem.txt".
# Then read it back and print it to the screen.


# ── Exercise 2 ────────────────────────────────────────────────
# Append a new line to the file "poem.txt" you created above.
# Read the file again and confirm the new line is there.


# ── Exercise 3 ────────────────────────────────────────────────
# Read the file "students.csv" using the csv module.
# Print each student's name and score in the format:
#   "Alice scored 88"


# ── Exercise 4 ────────────────────────────────────────────────
# Read students.csv and calculate:
#   a) The average score
#   b) The highest scorer's name and score
#   c) The lowest scorer's name and score
# Print all three results.


# ── Exercise 5 ────────────────────────────────────────────────
# Write a new CSV file called "results.csv" with two columns:
#   name, result
# where result is "PASS" if score >= 75, otherwise "FAIL".
# Use the data from students.csv.


# ── Exercise 6 (Stretch) ──────────────────────────────────────
# Count how many times each word appears in "poem.txt" (case-insensitive).
# Write a summary to "word_count.txt", one line per word:
#   "the: 3"
# Sort alphabetically.
