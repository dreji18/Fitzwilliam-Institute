# demo_03_control_flow.py
# Python 101 — Week 03 Live Demo: Control Flow

# ── Basic if/elif/else ────────────────────────────────────────
x = 42
if x > 100:
    print("big")
elif x > 10:
    print("medium")   # ← this runs
else:
    print("small")

# ── Comparison operators ──────────────────────────────────────
print(5 == 5)    # True    equal
print(5 != 4)    # True    not equal
print(5 > 3)     # True    greater than
print(5 >= 5)    # True    greater than or equal
print(3 < 5)     # True    less than
print("a" < "b") # True    strings compare lexicographically

# ── Logical operators ────────────────────────────────────────
age = 20
print(age >= 18 and age < 65)  # True  — working age
print(age < 18 or age >= 65)   # False — not working age
print(not (age < 18))          # True

# ── Truthiness ───────────────────────────────────────────────
# These are all "falsy" in Python:
for val in [0, 0.0, "", [], {}, None, False]:
    if not val:
        print(repr(val), "is falsy")

# ── Ternary (one-liner if) ────────────────────────────────────
score = 72
result = "pass" if score >= 50 else "fail"
print(f"Result: {result}")
