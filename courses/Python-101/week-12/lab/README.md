# Week 12 — Capstone Project: Student Grade Manager

**Topic:** Bringing it all together — file I/O, OOP, error handling, modules, functions

---

## Project Brief

Build a **command-line Student Grade Manager** that lets a teacher:

1. Add students and their scores
2. View all students and their averages
3. Search for a student by name
4. Save and load data from a JSON file
5. Print a grade report sorted by average

---

## Skills Covered

| Concept | Where it's used |
|---------|----------------|
| Functions | All menu actions |
| OOP | `Student` class |
| File I/O / JSON | Save & load data |
| Error handling | Invalid inputs, missing files |
| Lists & dicts | Storing student records |
| Modules | json, os, datetime |
| String formatting | Grade report output |

---

## Getting Started

1. Open `capstone_starter.py` — this is your starting point
2. Read all the comments — they outline what each function should do
3. Implement the functions one at a time
4. Test as you go: you don't need to finish everything before testing

## Stretch Goals

- Add a subject-by-subject breakdown in the report
- Sort students by name OR by average (user's choice)
- Validate that scores are between 0–100
- Track the date each score was added using the datetime module
- Colour-code output by grade band using ANSI escape codes

---

## Example Session

```
=== Student Grade Manager ===
1. Add student
2. Add score for student
3. View all students
4. Search student
5. Save
6. Load
7. Print report
8. Exit

> 1
Student name: Alice
Alice added.

> 2
Student name: Alice
Subject: Python 101
Score: 88
Score added.

> 3
Alice  | Python 101: 88 | Average: 88.0
```
