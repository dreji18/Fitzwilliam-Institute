# lab_06_solutions.py
# Python 101 — Week 06 — SOLUTIONS
# ⚠️  STAFF ONLY

# Exercise 1
scores = [88, 72, 95, 61, 84, 77, 90, 55, 68, 91]
print(scores[0], scores[-1])   # 88 91
print(scores[-3:])              # [55, 68, 91]
print(scores[::2])              # [88, 95, 84, 90, 68]

# Exercise 2
shopping = []
shopping.append("milk")
shopping.append("eggs")
shopping.append("bread")
shopping.append("butter")
shopping.insert(1, "coffee")
shopping.remove("bread")
shopping.sort()
print(shopping)  # ['butter', 'coffee', 'eggs', 'milk']

# Exercise 3
scores = [88, 72, 95, 61, 84, 77, 90, 55, 68, 91]
high_scores = [s for s in scores if s > 75]
print(high_scores)  # [88, 95, 84, 77, 90, 91]

# Exercise 4
squares = [n ** 2 for n in range(1, 11)]
print(squares)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# Exercise 5
student = ("Emma", 21, "Python 101")
name, age, course = student
print(f"{name} is {age} years old and is studying {course}.")

# Exercise 6
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Exercise 7 (Stretch)
dupes = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
seen = []
for item in dupes:
    if item not in seen:
        seen.append(item)
print(seen)  # [3, 1, 4, 5, 9, 2, 6]
