# demo_08_files.py
# Python 101 — Week 08 Live Demo: File I/O

import csv

# ── Writing a text file ───────────────────────────────────────
with open("demo_output.txt", "w") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.writelines(["Line 3\n", "Line 4\n"])

# ── Reading a text file ───────────────────────────────────────
with open("demo_output.txt") as f:
    content = f.read()           # whole file as one string
print(content)

with open("demo_output.txt") as f:
    lines = f.readlines()        # list of lines
print(lines)

with open("demo_output.txt") as f:
    for line in f:               # memory-efficient, line by line
        print(line.strip())

# ── File modes ───────────────────────────────────────────────
# "r"  read (default)
# "w"  write (overwrites)
# "a"  append
# "x"  create new (errors if exists)

# ── CSV writing ───────────────────────────────────────────────
data = [["name", "score"], ["Alice", 88], ["Bob", 72]]
with open("demo_scores.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

# ── CSV reading ───────────────────────────────────────────────
with open("demo_scores.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["score"])
