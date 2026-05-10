# demo_06_lists.py
# Python 101 — Week 06 Live Demo: Lists & Tuples

# ── List basics ───────────────────────────────────────────────
nums = [10, 20, 30, 40, 50]
print(nums[0])     # 10  (first)
print(nums[-1])    # 50  (last)
print(nums[1:3])   # [20, 30]  (slice)
print(nums[::-1])  # [50,40,30,20,10]  (reversed)

# ── Mutating a list ───────────────────────────────────────────
nums.append(60)
nums.insert(0, 5)
nums.pop()          # removes last
nums.remove(30)     # removes first occurrence
nums.sort()
print(nums)

# ── List comprehension ────────────────────────────────────────
evens   = [n for n in range(20) if n % 2 == 0]
doubled = [n * 2 for n in range(1, 6)]
words   = ["hello", "world", "python"]
upper   = [w.upper() for w in words]
print(evens, doubled, upper)

# ── Tuples ────────────────────────────────────────────────────
point = (3, 7)          # immutable
x, y  = point           # unpacking
print(f"x={x}, y={y}")

rgb = (255, 128, 0)
r, g, b = rgb
print(f"Red={r} Green={g} Blue={b}")
