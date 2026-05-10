# demo_07_dicts.py
# Python 101 — Week 07 Live Demo: Dictionaries & Sets

# ── Dictionary creation & access ──────────────────────────────
person = {"name": "Alice", "age": 30, "city": "Dublin"}
print(person["name"])               # Alice
print(person.get("country", "N/A")) # N/A  (safe access with default)

# ── Mutating a dict ───────────────────────────────────────────
person["age"] = 31                  # update
person["email"] = "alice@mail.ie"   # add new key
del person["city"]                  # delete
print(person)

# ── Iterating ────────────────────────────────────────────────
for key, value in person.items():
    print(f"{key}: {value}")

# ── Dict comprehension ────────────────────────────────────────
squares = {n: n**2 for n in range(1, 6)}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# ── Sets ─────────────────────────────────────────────────────
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a | b)    # union:        {1,2,3,4,5,6}
print(a & b)    # intersection: {3,4}
print(a - b)    # difference:   {1,2}
print(a ^ b)    # symmetric diff: {1,2,5,6}
