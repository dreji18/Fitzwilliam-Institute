# lab_10_solutions.py
# Python 101 — Week 10 — SOLUTIONS
# ⚠️  STAFF ONLY

import math
import random
import os
import json
from datetime import datetime, date, timedelta

# Exercise 1
print(f"Pi: {math.pi:.5f}")
print(f"Hypotenuse: {math.hypot(3, 4)}")
print(f"Floor 7.6: {math.floor(7.6)}")
print(f"Ceil 7.2:  {math.ceil(7.2)}")

# Exercise 2
items = ["apple", "banana", "cherry", "date", "elderberry"]
randoms = [random.randint(1, 100) for _ in range(5)]
print("5 random ints:", randoms)
print("Random item:", random.choice(items))
random.shuffle(items)
print("Shuffled:", items)

# Exercise 3
today     = date.today()
in_100    = today + timedelta(days=100)
next_year = date(today.year + 1, 1, 1)
days_left = (next_year - today).days
print("Today:", today)
print("100 days from now:", in_100)
print("Days until new year:", days_left)

# Exercise 4
print("CWD:", os.getcwd())
print("Files:", os.listdir("."))
csv_path = os.path.join("..", "..", "week-08", "lab", "students.csv")
print("students.csv exists:", os.path.exists(csv_path))

# Exercise 5
student = {
    "name": "Alice",
    "age": 21,
    "courses": ["Python 101", "Web Dev"],
    "scores": {"Python 101": 88, "Web Dev": 74},
}
json_str = json.dumps(student, indent=2)
print(json_str)

with open("student.json", "w") as f:
    f.write(json_str)

with open("student.json") as f:
    loaded = json.loads(f.read())
print("Loaded name:", loaded["name"])

# Exercise 6 (Stretch)
main   = sorted(random.sample(range(1, 51), 6))
bonus  = random.randint(1, 20)
print("Lucky numbers:", " ".join(str(n) for n in main), "| Bonus:", bonus)
