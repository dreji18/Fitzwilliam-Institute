# Data Analytics - Interactive Apps
**Fitzwilliam Institute · Deepak John Reji · 2026**

A collection of interactive Streamlit apps for the Diploma in Data Analytics course.

---

## Apps

| App | Lecture | Topic |
|-----|---------|-------|
| 🎲 Probability | Lecture 4 | Probability, Distributions, CLT |
| 📐 Statistical Testing | Lecture 6 | Confidence Intervals, Hypothesis Testing |
| 🔬 Two Samples | Lecture 7 | F-test, t-tests, Goodness of Fit |
| 🎮 MLR Quest | Lecture 8 | Multiple Linear Regression (gamified) |

---

## Deploy to Streamlit Cloud

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial deploy"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **New app**
3. Connect your GitHub account and select this repo
4. Set **Main file path** to: `Home.py`
5. Click **Deploy**

That's it - Streamlit Cloud installs all dependencies automatically from `requirements.txt`.

---

## Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run Home.py
```

---

## Repo Structure

```
├── Home.py                        ← Landing page (set this as main file)
├── requirements.txt               ← All Python dependencies
├── .streamlit/
│   └── config.toml                ← Theme and server settings
└── pages/
    ├── 1_🎲_Probability.py        ← Lecture 4
    ├── 2_📐_Statistical_Testing.py ← Lecture 6
    ├── 3_🔬_Two_Samples.py        ← Lecture 7
    └── 4_🎮_MLR_Quest.py          ← Lecture 8
```

Files in `pages/` are automatically picked up by Streamlit's multi-page routing —
no extra configuration needed.

---

## Adding More Apps

To add a new lecture app:

1. Drop the `.py` file into `pages/`
2. Name it `5_📊_Your_App_Name.py` (the number controls sidebar order)
3. Push to GitHub — Streamlit Cloud redeploys automatically

---

## Dependencies

| Package | Used by |
|---------|---------|
| `streamlit` | All apps |
| `numpy` | All apps |
| `pandas` | Two Samples, MLR Quest |
| `scipy` | Probability, Statistical Testing, Two Samples |
| `matplotlib` | Statistical Testing, Two Samples |
| `plotly` | Probability, MLR Quest |
