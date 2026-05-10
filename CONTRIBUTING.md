# Contributing Guide

Thank you for contributing to the Fitzwilliam Institute teaching repository. This guide covers everything you need to add a new course, upload weekly content, and submit changes cleanly.

---

## Table of Contents

- [Adding a New Course](#adding-a-new-course)
- [Adding Weekly Content](#adding-weekly-content)
- [Naming Conventions](#naming-conventions)
- [Submitting Changes](#submitting-changes)
- [Solutions Policy](#solutions-policy)

---

## Adding a New Course

1. Copy the `_template` folder into `courses/` and rename it:
   ```bash
   cp -r courses/_template courses/your-course-name
   ```
2. Edit `courses/your-course-name/README.md` with your course details.
3. Add your course to the table in the root `README.md`.
4. Open a pull request — see [Submitting Changes](#submitting-changes).

---

## Adding Weekly Content

Each week follows a fixed three-folder structure:

```
week-NN/
├── lab/          # Starter files — what students work from in class
├── solutions/    # Completed solutions — do NOT share with students
└── examples/     # Standalone demo scripts shown during the lecture
```

To add a new week, copy the template week folder from your course:
```bash
cp -r courses/_template/week-01 courses/your-course/week-03
```

Then add your files and open a pull request.

---

## Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Course folders | `kebab-case` | `web-dev-fundamentals` |
| Week folders | `week-NN` (zero-padded) | `week-01`, `week-12` |
| Python files | `snake_case.py` | `data_cleaning_lab.py` |
| Notebooks | `snake_case.ipynb` | `intro_to_pandas.ipynb` |
| Datasets | `snake_case.csv / .json` | `sample_students.csv` |

---

## Submitting Changes

1. **Create a branch** from `main`:
   ```bash
   git checkout -b course/python-101/week-03
   ```
   Branch naming: `course/<course-name>/week-NN` or `fix/<short-description>`

2. **Commit your changes** with a clear message:
   ```bash
   git add .
   git commit -m "Add Python 101 Week 03 lab and examples"
   ```

3. **Push and open a pull request**:
   ```bash
   git push origin course/python-101/week-03
   ```
   Then open a PR on GitHub. Use the PR template provided.

4. **Request a review** from at least one other staff member before merging.

---

## Solutions Policy

Solutions live in `solutions/` folders within each week. To prevent students from accessing them:

- Never commit solutions to a public-facing branch without discussion.
- Consider keeping solutions on a separate `solutions` branch with restricted push access.
- If the repo is public, solutions should live in a separate **private** repository.

---

## Questions?

Open an issue using the [Content Request template](./.github/ISSUE_TEMPLATE/content-request.md) or reach out directly.
