# demo_04_loops.py
# Python 101 — Week 04 Live Demo: Loops

# ── for loop over a list ──────────────────────────────────────
colours = ["red", "green", "blue"]
for colour in colours:
    print(colour.upper())

# ── range() ──────────────────────────────────────────────────
print(list(range(5)))          # [0,1,2,3,4]
print(list(range(1, 6)))       # [1,2,3,4,5]
print(list(range(0, 10, 2)))   # [0,2,4,6,8]  (step=2)
print(list(range(10, 0, -1)))  # [10,9,...,1] (count down)

# ── enumerate ────────────────────────────────────────────────
for idx, colour in enumerate(colours, start=1):
    print(f"{idx}: {colour}")

# ── while loop ───────────────────────────────────────────────
count = 0
while count < 5:
    print("count =", count)
    count += 1

# ── break & continue ─────────────────────────────────────────
for n in range(10):
    if n == 3:
        continue   # skip 3
    if n == 7:
        break      # stop at 7
    print(n)       # prints 0,1,2,4,5,6

# ── Accumulator pattern ───────────────────────────────────────
total = 0
for n in range(1, 6):
    total += n
print("Sum 1-5 =", total)   # 15
