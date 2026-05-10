# capstone_starter.py
# Python 101 — Week 12 Capstone: Student Grade Manager
# Fitzwilliam Institute
#
# Complete each function below. Don't change the function signatures.
# You can add helper functions if you need them.

import json
import os
from datetime import datetime


# ─────────────────────────────────────────────────────────────
# Student class
# ─────────────────────────────────────────────────────────────

class Student:
    """Represents a single student with a name and a dict of subject scores."""

    def __init__(self, name):
        # TODO: store name, initialise empty scores dict
        pass

    def add_score(self, subject, score):
        # TODO: add subject: score to self.scores
        pass

    def average(self):
        # TODO: return mean of scores, or 0.0 if no scores
        pass

    def grade(self):
        # TODO: return letter grade based on average()
        # A: 90+, B: 80-89, C: 70-79, D: 60-69, F: below 60
        pass

    def to_dict(self):
        # TODO: return a dict representation for JSON serialisation
        # {"name": ..., "scores": {...}}
        pass

    @classmethod
    def from_dict(cls, data):
        # TODO: create a Student from a dict (reverse of to_dict)
        pass

    def __str__(self):
        # TODO: "Alice | Avg: 85.0 (B) | Subjects: Python 101, Web Dev"
        pass


# ─────────────────────────────────────────────────────────────
# Data management functions
# ─────────────────────────────────────────────────────────────

def find_student(students, name):
    """Return the Student object with the given name, or None."""
    # TODO
    pass


def save_data(students, filename="grades.json"):
    """Save list of Student objects to a JSON file."""
    # TODO
    pass


def load_data(filename="grades.json"):
    """Load students from a JSON file. Return empty list if file not found."""
    # TODO
    pass


# ─────────────────────────────────────────────────────────────
# Report
# ─────────────────────────────────────────────────────────────

def print_report(students):
    """Print a formatted grade report sorted by average (highest first)."""
    # TODO
    # Example output:
    # ══════════════════════════════════
    #  GRADE REPORT — 15 January 2024
    # ══════════════════════════════════
    #  1. Alice      │ Avg: 88.0 │ A
    #  2. Charlie    │ Avg: 79.5 │ C
    # ══════════════════════════════════
    pass


# ─────────────────────────────────────────────────────────────
# Menu
# ─────────────────────────────────────────────────────────────

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
            print("Saved.")

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
