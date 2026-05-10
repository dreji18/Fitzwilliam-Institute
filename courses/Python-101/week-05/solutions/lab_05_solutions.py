# lab_05_solutions.py
# Python 101 — Week 05 — SOLUTIONS
# ⚠️  STAFF ONLY

# Exercise 1
def greet(name):
    """Print a greeting for the given name."""
    print(f"Hello, {name}!")

greet("Alice")

# Exercise 2
def celsius_to_fahrenheit(c):
    """Convert Celsius to Fahrenheit."""
    return (c * 9 / 5) + 32

for temp in [0, 100, 37]:
    print(f"{temp}°C = {celsius_to_fahrenheit(temp):.1f}°F")

# Exercise 3
def calculate_area(shape, a, b=None):
    """Return the area of a rectangle or triangle."""
    if shape == "rectangle":
        return a * b
    elif shape == "triangle":
        return 0.5 * a * b
    return None

print(calculate_area("rectangle", 5, 3))  # 15
print(calculate_area("triangle", 6, 4))   # 12.0

# Exercise 4
def is_prime(n):
    """Return True if n is a prime number."""
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

for num in [2, 7, 9, 13, 25]:
    print(f"{num} is prime: {is_prime(num)}")

# Exercise 5
def summarise(numbers):
    """Return a stats summary of a list of numbers."""
    return {
        "count":   len(numbers),
        "sum":     sum(numbers),
        "min":     min(numbers),
        "max":     max(numbers),
        "average": sum(numbers) / len(numbers),
    }

print(summarise([4, 8, 15, 16, 23, 42]))

# Exercise 6 (Stretch)
def fizzbuzz(n):
    """Return FizzBuzz list for 1..n."""
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result

print(fizzbuzz(20))
