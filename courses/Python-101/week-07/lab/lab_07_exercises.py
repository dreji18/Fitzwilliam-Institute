# lab_07_exercises.py
# Python 101 — Week 07: Dictionaries & Sets
# Fitzwilliam Institute

# ── Exercise 1 ────────────────────────────────────────────────
# Create a dictionary for a student with keys:
#   name, age, course, grade
# Then:
#   a) Print the student's name
#   b) Update the grade to "A"
#   c) Add a new key: email = "student@fitzwilliam.ie"
#   d) Print all keys, then all values


# ── Exercise 2 ────────────────────────────────────────────────
# Count how many times each word appears in the sentence.
# Store results in a dictionary and print it.
sentence = "the cat sat on the mat and the cat slept"


# ── Exercise 3 ────────────────────────────────────────────────
# Given the contacts dictionary, find everyone who lives in "Dublin".
# Print their names.
contacts = {
    "Alice":   {"city": "Dublin",  "phone": "087-111-2222"},
    "Bob":     {"city": "Cork",    "phone": "086-333-4444"},
    "Charlie": {"city": "Dublin",  "phone": "085-555-6666"},
    "Diana":   {"city": "Galway",  "phone": "089-777-8888"},
}


# ── Exercise 4 ────────────────────────────────────────────────
# Use a set to find:
#   a) Students in both Python AND Web Dev (intersection)
#   b) Students in Python but NOT Web Dev (difference)
#   c) All unique students across both courses (union)
python_students  = {"Alice", "Bob", "Charlie", "Diana", "Eve"}
webdev_students  = {"Bob", "Diana", "Frank", "Grace"}


# ── Exercise 5 ────────────────────────────────────────────────
# Given a list of words, use a dictionary comprehension to create a
# dictionary mapping each word to its length.
words = ["apple", "banana", "cherry", "date", "elderberry"]


# ── Exercise 6 (Stretch) ──────────────────────────────────────
# Given a list of exam results (name, score), build a dictionary that
# groups names by grade band: "A" (90+), "B" (80-89), "C" (70-79), "F" (<70)
results = [
    ("Alice", 92), ("Bob", 74), ("Charlie", 85),
    ("Diana", 91), ("Eve", 67), ("Frank", 80),
]
