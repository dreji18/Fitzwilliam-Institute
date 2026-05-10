# demo_02_types.py
# Python 101 — Week 02 Live Demo: Data Types & Strings

# ── Type conversion ──────────────────────────────────────────
x = "42"
print(type(x), x + "1")        # str concatenation: "421"
x = int(x)
print(type(x), x + 1)          # int addition: 43
print(float(x))                 # 42.0
print(bool(0), bool(1), bool(""), bool("hi"))

# ── f-strings ────────────────────────────────────────────────
name  = "Bob"
score = 87.5
print(f"Name: {name:<10} Score: {score:>7.2f}")  # alignment + decimals
print(f"Score is {'PASS' if score >= 50 else 'FAIL'}")  # inline expression

# ── String methods ────────────────────────────────────────────
s = "  fitzwilliam institute  "
print(s.strip().title())         # Fitzwilliam Institute
print(s.strip().split())         # ['fitzwilliam', 'institute']

# ── Slicing ──────────────────────────────────────────────────
word = "programming"
print(word[0])      # p
print(word[-1])     # g
print(word[0:4])    # prog
print(word[::2])    # pormig  (every second char)
print(word[::-1])   # gnimmargorp  (reversed)
