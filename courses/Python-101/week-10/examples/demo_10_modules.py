# demo_10_modules.py
# Python 101 — Week 10 Live Demo: Modules & Packages

import math
import random
import json
import os
from datetime import datetime, timedelta

# ── math ─────────────────────────────────────────────────────
print(math.pi)
print(math.sqrt(144))    # 12.0
print(math.log(100, 10)) # 2.0  (log base 10)
print(math.factorial(5)) # 120

# ── random ───────────────────────────────────────────────────
print(random.random())              # 0.0 – 1.0
print(random.randint(1, 6))        # dice roll
print(random.choice(["a","b","c"])) # pick one

# ── datetime ─────────────────────────────────────────────────
now = datetime.now()
print(now.strftime("%A, %d %B %Y"))   # "Monday, 15 January 2024"
tomorrow = now + timedelta(days=1)
print(tomorrow.date())

# ── json ─────────────────────────────────────────────────────
data = {"name": "Alice", "scores": [88, 92, 79]}
s    = json.dumps(data, indent=2)          # dict → string
print(s)
back = json.loads(s)                       # string → dict
print(back["name"])

# ── os ───────────────────────────────────────────────────────
print(os.getcwd())
print(os.path.exists("some_file.txt"))
print(os.path.join("folder", "subfolder", "file.txt"))
