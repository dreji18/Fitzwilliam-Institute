# demo_05_functions.py
# Python 101 — Week 05 Live Demo: Functions

# ── Basic function ────────────────────────────────────────────
def add(a, b):
    """Return the sum of a and b."""
    return a + b

result = add(3, 4)
print(result)  # 7

# ── Default arguments ─────────────────────────────────────────
def power(base, exponent=2):
    return base ** exponent

print(power(3))      # 9  (exponent defaults to 2)
print(power(3, 3))   # 27

# ── Keyword arguments ─────────────────────────────────────────
def describe_pet(animal, name):
    print(f"{name} is a {animal}")

describe_pet(name="Whiskers", animal="cat")  # order doesn't matter

# ── Multiple return values (via tuple) ───────────────────────
def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([3, 1, 4, 1, 5, 9])
print(lo, hi)   # 1 9

# ── Scope ────────────────────────────────────────────────────
x = "global"

def show_scope():
    x = "local"     # different variable!
    print(x)        # local

show_scope()
print(x)            # global  (unchanged)
