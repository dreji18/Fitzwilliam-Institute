# demo_09_errors.py
# Python 101 — Week 09 Live Demo: Error Handling

# ── Basic try/except ──────────────────────────────────────────
try:
    x = int("not a number")
except ValueError as e:
    print(f"Caught ValueError: {e}")

# ── Multiple except blocks ────────────────────────────────────
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return None
    except TypeError:
        print("Both arguments must be numbers!")
        return None
    else:
        print("Division succeeded!")
        return result
    finally:
        print("(safe_divide finished)")

safe_divide(10, 2)
safe_divide(10, 0)
safe_divide(10, "x")

# ── Raising exceptions ────────────────────────────────────────
def set_speed(speed):
    if speed < 0:
        raise ValueError(f"Speed cannot be negative: {speed}")
    if speed > 200:
        raise ValueError(f"Speed too high: {speed}")
    return speed

try:
    set_speed(-10)
except ValueError as e:
    print(f"Error: {e}")

# ── Custom exception ──────────────────────────────────────────
class InvalidEmailError(Exception):
    pass

def validate_email(email):
    if "@" not in email:
        raise InvalidEmailError(f"'{email}' is not a valid email")
    return email

try:
    validate_email("notanemail")
except InvalidEmailError as e:
    print(f"Email error: {e}")
