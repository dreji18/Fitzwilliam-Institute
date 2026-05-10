# lab_09_solutions.py
# Python 101 — Week 09 — SOLUTIONS
# ⚠️  STAFF ONLY

# Exercise 1
try:
    result = 10 / 0
    print(result)
except ZeroDivisionError:
    print("Error: cannot divide by zero")

# Exercise 2
def safe_int(value):
    """Try to convert value to int; return None on failure."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

for v in ["42", "hello", "3.14", True]:
    print(f"safe_int({v!r}) = {safe_int(v)}")

# Exercise 3
def read_score(filename):
    try:
        with open(filename) as f:
            line = f.readline().strip()
        return float(line)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filename}")
    except ValueError:
        raise ValueError(f"Could not convert '{line}' to a number.")
    finally:
        print("Attempt complete.")

# Exercise 4
def validate_age(age):
    if not isinstance(age, int):
        raise TypeError(f"Age must be an integer, got {type(age).__name__}")
    if not 0 <= age <= 130:
        raise ValueError(f"Age must be between 0 and 130, got {age}")
    return age

for test in [25, "twenty", -5, 200]:
    try:
        print(validate_age(test))
    except (TypeError, ValueError) as e:
        print(f"Validation error: {e}")

# Exercise 5
class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the account balance."""
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(
            f"Cannot withdraw €{amount:.2f}: balance is only €{balance:.2f}"
        )
    return balance - amount

try:
    print(withdraw(100, 40))   # 60
    print(withdraw(60, 80))    # raises
except InsufficientFundsError as e:
    print(e)

# Exercise 6 (Stretch)
def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("That's not a valid integer. Try again.")

# num = get_positive_int("Enter a positive number: ")
# print(f"You entered: {num}")
