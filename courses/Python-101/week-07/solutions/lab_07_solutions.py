# lab_07_solutions.py
# Python 101 — Week 07 — SOLUTIONS
# ⚠️  STAFF ONLY

# Exercise 1
student = {"name": "Alice", "age": 21, "course": "Python 101", "grade": "B"}
print(student["name"])
student["grade"] = "A"
student["email"] = "student@fitzwilliam.ie"
print(list(student.keys()))
print(list(student.values()))

# Exercise 2
sentence = "the cat sat on the mat and the cat slept"
word_count = {}
for word in sentence.split():
    word_count[word] = word_count.get(word, 0) + 1
print(word_count)

# Exercise 3
contacts = {
    "Alice":   {"city": "Dublin",  "phone": "087-111-2222"},
    "Bob":     {"city": "Cork",    "phone": "086-333-4444"},
    "Charlie": {"city": "Dublin",  "phone": "085-555-6666"},
    "Diana":   {"city": "Galway",  "phone": "089-777-8888"},
}
dublin_contacts = [name for name, info in contacts.items() if info["city"] == "Dublin"]
print(dublin_contacts)  # ['Alice', 'Charlie']

# Exercise 4
python_students = {"Alice", "Bob", "Charlie", "Diana", "Eve"}
webdev_students = {"Bob", "Diana", "Frank", "Grace"}
print("Both:", python_students & webdev_students)
print("Python only:", python_students - webdev_students)
print("All:", python_students | webdev_students)

# Exercise 5
words = ["apple", "banana", "cherry", "date", "elderberry"]
word_lengths = {word: len(word) for word in words}
print(word_lengths)

# Exercise 6 (Stretch)
results = [
    ("Alice", 92), ("Bob", 74), ("Charlie", 85),
    ("Diana", 91), ("Eve", 67), ("Frank", 80),
]
bands = {"A": [], "B": [], "C": [], "F": []}
for name, score in results:
    if score >= 90:
        bands["A"].append(name)
    elif score >= 80:
        bands["B"].append(name)
    elif score >= 70:
        bands["C"].append(name)
    else:
        bands["F"].append(name)
print(bands)
