# lab_08_solutions.py
# Python 101 — Week 08 — SOLUTIONS
# ⚠️  STAFF ONLY

import csv

# Exercise 1
poem = """Roses are red,
Violets are blue,
Python is wonderful,
And so are you."""

with open("poem.txt", "w") as f:
    f.write(poem)

with open("poem.txt", "r") as f:
    print(f.read())

# Exercise 2
with open("poem.txt", "a") as f:
    f.write("\nKeep coding every day.\n")

with open("poem.txt", "r") as f:
    print(f.read())

# Exercise 3
with open("students.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['name']} scored {row['score']}")

# Exercise 4
with open("students.csv", newline="") as f:
    reader = csv.DictReader(f)
    students = list(reader)

scores = [(s["name"], int(s["score"])) for s in students]
total  = sum(s for _, s in scores)
avg    = total / len(scores)
top    = max(scores, key=lambda x: x[1])
bot    = min(scores, key=lambda x: x[1])
print(f"Average: {avg:.1f}")
print(f"Highest: {top[0]} with {top[1]}")
print(f"Lowest:  {bot[0]} with {bot[1]}")

# Exercise 5
with open("students.csv", newline="") as fin, open("results.csv", "w", newline="") as fout:
    reader = csv.DictReader(fin)
    writer = csv.writer(fout)
    writer.writerow(["name", "result"])
    for row in reader:
        result = "PASS" if int(row["score"]) >= 75 else "FAIL"
        writer.writerow([row["name"], result])
print("results.csv written.")

# Exercise 6 (Stretch)
with open("poem.txt") as f:
    words = f.read().lower().split()

word_count = {}
for word in words:
    clean = word.strip(".,!?\"'")
    word_count[clean] = word_count.get(clean, 0) + 1

with open("word_count.txt", "w") as f:
    for word in sorted(word_count):
        f.write(f"{word}: {word_count[word]}\n")
print("word_count.txt written.")
