# lab_11_solutions.py
# Python 101 — Week 11 — SOLUTIONS
# ⚠️  STAFF ONLY

# Exercise 1
class Rectangle:
    def __init__(self, width, height):
        self.width  = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def __str__(self):
        return f"Rectangle({self.width}x{self.height})"

r1 = Rectangle(5, 3)
r2 = Rectangle(10, 4)
for r in [r1, r2]:
    print(r, "area:", r.area(), "perimeter:", r.perimeter())

# Exercise 2
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner   = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited €{amount:.2f}. New balance: €{self.balance:.2f}")

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError(f"Insufficient funds: balance is €{self.balance:.2f}")
        self.balance -= amount
        print(f"Withdrew €{amount:.2f}. New balance: €{self.balance:.2f}")

    def __str__(self):
        return f"BankAccount(owner={self.owner}, balance=€{self.balance:.2f})"

acc = BankAccount("Alice")
acc.deposit(200)
acc.withdraw(50)
print(acc)
try:
    acc.withdraw(500)
except ValueError as e:
    print(f"Error: {e}")

# Exercise 3
class Animal:
    def __init__(self, name, sound):
        self.name  = name
        self.sound = sound

    def speak(self):
        print(f"{self.name} says {self.sound}!")

class Dog(Animal):
    def __init__(self, name):
        super().__init__(name, "Woof")

    def fetch(self, item):
        print(f"{self.name} fetches the {item}!")

class Cat(Animal):
    def __init__(self, name):
        super().__init__(name, "Meow")

Animal("Generic Beast", "Roar").speak()
Dog("Rex").speak()
Dog("Rex").fetch("ball")
Cat("Whiskers").speak()

# Exercise 4
class Student:
    def __init__(self, name, student_id):
        self.name       = name
        self.student_id = student_id
        self.grades     = {}

    def add_grade(self, subject, score):
        self.grades[subject] = score

    def average(self):
        if not self.grades:
            return 0
        return sum(self.grades.values()) / len(self.grades)

    def __str__(self):
        return f"Student: {self.name} (ID: {self.student_id}) | Avg: {self.average():.1f}"

s = Student("Alice", "S001")
s.add_grade("Python 101", 88)
s.add_grade("Web Dev", 74)
s.add_grade("Databases", 91)
print(s)

# Exercise 5 (Stretch)
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek at empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return f"Stack({self._items})"

st = Stack()
st.push(1); st.push(2); st.push(3)
print(st)              # Stack([1, 2, 3])
print(st.peek())       # 3
print(st.pop())        # 3
print(len(st))         # 2
