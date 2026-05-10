# lab_09_exercises.py
# Python 101 — Week 09: Error Handling
# Fitzwilliam Institute

# ── Exercise 1 ────────────────────────────────────────────────
# The code below will crash. Wrap it in a try/except block so it
# prints "Error: cannot divide by zero" instead of crashing.
result = 10 / 0
print(result)


# ── Exercise 2 ────────────────────────────────────────────────
# Write a function called safe_int(value) that:
#   - Tries to convert value to int
#   - Returns the integer if successful
#   - Returns None if conversion fails (don't crash)
# Test it with: "42", "hello", "3.14", True


# ── Exercise 3 ────────────────────────────────────────────────
# Write a function called read_score(filename) that:
#   - Reads the first line of a file and returns it as a float
#   - Raises a FileNotFoundError message if the file doesn't exist
#   - Raises a ValueError message if the content isn't a valid number
#   - Uses a finally block to print "Attempt complete." always
# Test with a real file and a fake filename.


# ── Exercise 4 ────────────────────────────────────────────────
# Write a function called validate_age(age) that:
#   - Raises a TypeError if age is not an int
#   - Raises a ValueError if age is not between 0 and 130
#   - Returns age if valid
# Test all three cases.


# ── Exercise 5 ────────────────────────────────────────────────
# Create a custom exception class called InsufficientFundsError.
# Write a function called withdraw(balance, amount) that:
#   - Raises InsufficientFundsError if amount > balance
#   - Returns the new balance otherwise
# Test both cases.


# ── Exercise 6 (Stretch) ──────────────────────────────────────
# Write a robust function called get_positive_int(prompt) that:
#   - Asks the user for input using input()
#   - Keeps asking until the user enters a valid positive integer
#   - Handles non-integer input gracefully (catch ValueError)
# Call it with prompt="Enter a positive number: "
