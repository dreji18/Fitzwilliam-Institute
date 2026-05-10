# capstone_solution.py
# Python 101 — Week 12 Capstone — COMPLETE SOLUTION
# ⚠️  STAFF ONLY

import json
import os
from datetime import datetime


class Student:
    """Represents a single student with a name and a dict of subject scores."""

    def __init__(self, name):
        self.name   = name
        self.scores = {}   # {subject: score}

    def add_score(self, subject, score):
        self.scores[subject] = score

    def average(self):
        if not self.scores:
            return 0.0
        return sum(self.scores.values()) / len(self.scores)

    def grade(self):
        avg = self.average()
        if avg >= 90: return "A"
        if avg >= 80: return "B"
        if avg >= 70: return "C"
        if avg >= 60: return "D"
        return "F"

    def to_dict(self):
        return {"name": self.name, "scores": self.scores}

    @classmethod
    def from_dict(cls, data):
        s = cls(data["name"])
        s.scores = data["scores"]
        return s

    def __str__(self):
        subjects = ", ".join(self.scores.keys()) if self.scores else "none"
        return (f"{self.name:<12} | Avg: {self.average():>5.1f} ({self.grade()})"
                f" | Subjects: {subjects}")


def find_student(students, name):
    for s in students:
        if s.name.lower() == name.lower():
            return s
    return None


def save_data(students, filename="grades.json"):
    with open(filename, "w") as f:
        json.dump([s.to_dict() for s in students], f, indent=2)


def load_data(filename="grades.json"):
    try:
        with open(filename) as f:
            data = json.load(f)
        return [Student.from_dict(d) for d in data]
    except FileNotFoundError:
        return []


def print_report(students):
    if not students:
        print("No students to report.")
        return
    sorted_students = sorted(students, key=lambda s: s.average(), reverse=True)
    date_str = datetime.now().strftime("%d %B %Y")
    width = 42
    print("\n" + "═" * width)
    print(f"  GRADE REPORT — {date_str}")
    print("═" * width)
    for i, s in enumerate(sorted_students, 1):
        print(f"  {i:>2}. {s.name:<12} │ Avg: {s.average():>5.1f} │ {s.grade()}")
    print("═" * width)


def show_menu():
    print("\n=== Student Grade Manager ===")
    print("1. Add student")
    print("2. Add score for student")
    print("3. View all students")
    print("4. Search student")
    print("5. Save")
    print("6. Load")
    print("7. Print report")
    print("8. Exit")


def main():
    students = []

    while True:
        show_menu()
        choice = input("\n> ").strip()

        if choice == "1":
            name = input("Student name: ").strip()
            if find_student(students, name):
                print(f"{name} already exists.")
            else:
                students.append(Student(name))
                print(f"{name} added.")

        elif choice == "2":
            name    = input("Student name: ").strip()
            student = find_student(students, name)
            if not student:
                print(f"Student '{name}' not found.")
            else:
                subject = input("Subject: ").strip()
                try:
                    score = float(input("Score: "))
                    if not 0 <= score <= 100:
                        print("Score must be between 0 and 100.")
                    else:
                        student.add_score(subject, score)
                        print("Score added.")
                except ValueError:
                    print("Invalid score — must be a number.")

        elif choice == "3":
            if not students:
                print("No students yet.")
            for s in students:
                print(s)

        elif choice == "4":
            name    = input("Search name: ").strip()
            student = find_student(students, name)
            print(student if student else "Not found.")

        elif choice == "5":
            save_data(students)
            print("Saved to grades.json.")

        elif choice == "6":
            students = load_data()
            print(f"Loaded {len(students)} student(s).")

        elif choice == "7":
            print_report(students)

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Choose 1-8.")


if __name__ == "__main__":
    main()
