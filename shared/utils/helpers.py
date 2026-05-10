# helpers.py
# Fitzwilliam Institute — Shared Utilities
#
# Common helper functions available to all courses.
# Import in any lab or demo with:
#   import sys, os
#   sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../shared/utils'))
#   from helpers import greet, check_answer


def greet(name: str) -> None:
    """Print a welcome message for a student."""
    print(f"Welcome, {name}! Let's get coding.")


def check_answer(expected, actual, label: str = "Exercise") -> None:
    """
    Compare a student's answer to the expected value and print a result.

    Usage:
        check_answer(42, my_answer, "Exercise 1")
    """
    if expected == actual:
        print(f"✅  {label}: Correct! ({actual})")
    else:
        print(f"❌  {label}: Got {actual!r}, expected {expected!r}")


def section(title: str) -> None:
    """Print a visible section divider — useful in demo scripts."""
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")
