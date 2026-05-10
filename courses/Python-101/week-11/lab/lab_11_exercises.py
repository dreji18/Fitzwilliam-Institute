# lab_11_exercises.py
# Python 101 — Week 11: Object-Oriented Programming
# Fitzwilliam Institute

# ── Exercise 1 ────────────────────────────────────────────────
# Create a class called Rectangle with:
#   - __init__(self, width, height)
#   - area() method → returns width * height
#   - perimeter() method → returns 2 * (width + height)
#   - __str__ method → "Rectangle(5x3)"
# Create two rectangles and print their area, perimeter, and str representation.


# ── Exercise 2 ────────────────────────────────────────────────
# Create a class called BankAccount with:
#   - __init__(self, owner, balance=0)
#   - deposit(amount) → adds to balance, prints confirmation
#   - withdraw(amount) → subtracts from balance, raises ValueError if insufficient
#   - __str__ → "BankAccount(owner=Alice, balance=€150.00)"
# Test depositing and withdrawing, including an over-withdrawal attempt.


# ── Exercise 3 ────────────────────────────────────────────────
# Create a class called Animal with:
#   - __init__(self, name, sound)
#   - speak() → prints "[name] says [sound]!"
#
# Then create subclasses Dog and Cat that:
#   - Call the parent __init__ with the appropriate sound ("Woof", "Meow")
#   - Dog has an extra method: fetch(item) → prints "[name] fetches the [item]!"
#
# Create instances of all three and test them.


# ── Exercise 4 ────────────────────────────────────────────────
# Create a class called Student with:
#   - __init__(self, name, student_id)
#   - add_grade(subject, score) → stores in a dict
#   - average() → returns the mean score, or 0 if no grades
#   - __str__ → "Student: Alice (ID: S001) | Avg: 85.0"
# Test by adding multiple grades.


# ── Exercise 5 (Stretch) ──────────────────────────────────────
# Create a simple Stack class (Last-In-First-Out) with:
#   - push(item) → adds to top
#   - pop() → removes and returns top item; raises IndexError if empty
#   - peek() → returns top item without removing
#   - is_empty() → returns True if no items
#   - __len__ → returns number of items
#   - __str__ → shows items from bottom to top
# Test all methods.
