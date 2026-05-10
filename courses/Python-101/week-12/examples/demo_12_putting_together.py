# demo_12_putting_together.py
# Python 101 — Week 12 Live Demo: Putting It All Together
#
# A mini demonstration of combining: OOP, file I/O, error handling,
# modules, and list comprehensions in one cohesive script.

import json
from datetime import datetime


class ScoreCard:
    """A simple score card for one exam sitting."""

    def __init__(self, student_name, date=None):
        self.student_name = student_name
        self.date         = date or datetime.today().strftime("%Y-%m-%d")
        self._scores      = {}

    def add(self, subject, score):
        if not isinstance(score, (int, float)) or not 0 <= score <= 100:
            raise ValueError(f"Score must be 0-100, got {score}")
        self._scores[subject] = score

    def average(self):
        return sum(self._scores.values()) / len(self._scores) if self._scores else 0

    def passed(self, pass_mark=50):
        return all(s >= pass_mark for s in self._scores.values())

    def to_dict(self):
        return {"student": self.student_name, "date": self.date, "scores": self._scores}

    @classmethod
    def from_dict(cls, d):
        card = cls(d["student"], d.get("date"))
        for subj, score in d["scores"].items():
            card.add(subj, score)
        return card

    def __str__(self):
        lines = [f"Score Card — {self.student_name} ({self.date})"]
        for subj, score in self._scores.items():
            lines.append(f"  {subj:<20} {score:>6.1f}")
        lines.append(f"  {'Average':<20} {self.average():>6.1f}")
        lines.append(f"  {'Status':<20} {'PASS' if self.passed() else 'FAIL':>6}")
        return "\n".join(lines)


def save_cards(cards, path="scorecards.json"):
    with open(path, "w") as f:
        json.dump([c.to_dict() for c in cards], f, indent=2)
    print(f"Saved {len(cards)} card(s) to {path}")


def load_cards(path="scorecards.json"):
    try:
        with open(path) as f:
            return [ScoreCard.from_dict(d) for d in json.load(f)]
    except FileNotFoundError:
        print("No saved data found.")
        return []


# ── Demo run ─────────────────────────────────────────────────
if __name__ == "__main__":
    alice = ScoreCard("Alice")
    alice.add("Python 101", 88)
    alice.add("Web Dev",    74)
    alice.add("Databases",  91)

    bob = ScoreCard("Bob")
    bob.add("Python 101", 55)
    bob.add("Web Dev",    48)   # fail

    cards = [alice, bob]
    for card in cards:
        print(card)
        print()

    save_cards(cards)
    loaded = load_cards()
    print(f"\nLoaded {len(loaded)} card(s) back from file.")

    # Who passed?
    passed = [c.student_name for c in loaded if c.passed()]
    print("Passed:", passed)
