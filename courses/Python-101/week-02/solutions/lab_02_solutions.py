# lab_02_solutions.py
# Python 101 — Week 02 — SOLUTIONS
# ⚠️  STAFF ONLY

# Exercise 1
age_str = "28"
age = int(age_str) + 10
print(age)  # 38

# Exercise 2
name       = "Alice"
age        = 22
height_m   = 1.72
is_student = True
print(f"{name} is {age} years old, {height_m} m tall, and is a student: {is_student}")

# Exercise 3
sentence = "Python is easy to learn and fun to use."
print(sentence.upper())
print(sentence.lower())
print(sentence.lower().count('e'))      # 5
print(sentence.replace("Python", "coding"))

# Exercise 4
messy = "   Hello there, world!   "
clean = messy.strip()
print(clean)
print(clean.startswith("Hello"))        # True
print(clean.split())                    # ['Hello', 'there,', 'world!']

# Exercise 5
item  = "Notebook"
price = 4.5
qty   = 3
total = price * qty
print(f"{qty}x {item} @ €{price:.2f} each = €{total:.2f}")

# Exercise 6 (Stretch)
word = "racecar"
print(word == word[::-1])               # True
