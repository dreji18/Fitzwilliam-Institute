# Fitzwilliam Institute — Teaching Repository

A shared repository for course materials, code examples, and lab exercises across all tech and programming courses taught at Fitzwilliam Institute.

---

## Repository Structure

```
fitzwilliam-teaching/
├── courses/                  # One folder per course
│   ├── _template/            # Copy this when adding a new course
│   └── python-101/           # Example course
│       ├── README.md         # Course overview
│       ├── week-01/
│       │   ├── lab/          # Starter files for students
│       │   ├── solutions/    # Completed solutions (staff only)
│       │   └── examples/     # Live demo code from lectures
│       └── week-02/
│           └── ...
├── shared/                   # Reusable across all courses
│   ├── utils/                # Common helper scripts
│   ├── data/                 # Shared datasets
│   └── setup/                # Environment setup files
├── .github/
│   ├── ISSUE_TEMPLATE/       # Bug / content request templates
│   └── workflows/            # CI checks (linting etc.)
├── CONTRIBUTING.md
└── .gitignore
```

---

## Courses

| Course | Instructor | Status |
|--------|------------|--------|
| [Python 101](./courses/python-101/) | — | Active |

> To add a new course, see [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## Getting Started (Students)

1. Clone the repository:
   ```bash
   git clone https://github.com/fitzwilliam-institute/teaching.git
   cd teaching
   ```
2. Set up your environment:
   ```bash
   cd shared/setup
   pip install -r requirements.txt
   ```
3. Navigate to your course folder and follow the course README.

---

## Getting Started (Staff)

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to add a course, add weekly content, and submit changes via pull request.

---

## Contact

For questions about this repository, open a GitHub Issue using the appropriate template.
