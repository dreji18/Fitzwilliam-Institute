# demo_11_oop.py
# Python 101 — Week 11 Live Demo: Object-Oriented Programming

# ── Defining a class ──────────────────────────────────────────
class Circle:
    PI = 3.14159   # class attribute (shared)

    def __init__(self, radius):
        self.radius = radius    # instance attribute (unique per object)

    def area(self):
        return Circle.PI * self.radius ** 2

    def __str__(self):
        return f"Circle(r={self.radius})"

    def __repr__(self):
        return f"Circle({self.radius!r})"

c1 = Circle(5)
c2 = Circle(10)
print(c1)            # Circle(r=5)
print(c1.area())     # 78.53975
print(repr(c2))      # Circle(10)

# ── Inheritance ───────────────────────────────────────────────
class Shape:
    def __init__(self, colour="black"):
        self.colour = colour

    def describe(self):
        print(f"I am a {self.colour} {self.__class__.__name__}")

class Square(Shape):
    def __init__(self, side, colour="black"):
        super().__init__(colour)     # call parent __init__
        self.side = side

    def area(self):
        return self.side ** 2

sq = Square(4, colour="red")
sq.describe()         # I am a red Square
print(sq.area())      # 16
print(isinstance(sq, Shape))   # True — sq IS a Shape
