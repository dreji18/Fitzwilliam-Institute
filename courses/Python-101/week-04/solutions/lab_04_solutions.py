# lab_04_solutions.py
# Python 101 — Week 04 — SOLUTIONS
# ⚠️  STAFF ONLY

# Exercise 1
fruits = ["apple", "banana", "cherry", "date", "elderberry"]
for fruit in fruits:
    print(fruit)

# Exercise 2
for i in range(1, 13):
    print(f"7 x {i} = {7 * i}")

# Exercise 3
value = 1
while value <= 1000:
    value *= 2
    print(value)

# Exercise 4
fruits = ["apple", "banana", "cherry", "date", "elderberry"]
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# Exercise 5
for n in range(1, 51):
    if n % 3 == 0:
        continue
    if n >= 40:
        break
    print(n)

# Exercise 6
for row in range(5):
    print("* " * 5)

# Exercise 7 (Stretch)
total = 0
for n in range(1, 101):
    if n % 2 == 0:
        total += n
print("Sum of even numbers 1-100:", total)  # 2550
