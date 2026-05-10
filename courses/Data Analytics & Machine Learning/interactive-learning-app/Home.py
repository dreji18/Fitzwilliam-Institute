import streamlit as st

st.set_page_config(
    page_title="Data Analytics · Fitzwilliam Institute",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

.hero {
    padding: 2.5rem 0 2rem;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 2rem;
}
.hero-eyebrow {
    font-size: .75rem;
    letter-spacing: .2em;
    color: #5c7cfa;
    text-transform: uppercase;
    margin-bottom: .5rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -1.5px;
    margin: 0 0 .5rem;
    line-height: 1.1;
    color: #0f1b2d;
}
.hero h1 span {
    background: linear-gradient(120deg, #5c7cfa, #38d9a9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p { color: #666; font-size: .9rem; margin: 0; }

.app-card {
    background: #ffffff;
    border: 1px solid #e8ecff;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 12px rgba(92,124,250,.06);
    transition: box-shadow .2s;
}
.app-card:hover { box-shadow: 0 6px 24px rgba(92,124,250,.14); }
.app-card .icon { font-size: 2rem; margin-bottom: .5rem; }
.app-card h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #1a237e;
    margin: 0 0 .3rem;
}
.app-card .lecture-tag {
    font-size: .72rem;
    font-family: 'DM Mono', monospace;
    background: #f0f4ff;
    color: #5c7cfa;
    border-radius: 999px;
    padding: .2rem .7rem;
    display: inline-block;
    margin-bottom: .5rem;
}
.app-card p { color: #555; font-size: .83rem; line-height: 1.6; margin: 0; }

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Diploma in Data Analytics</div>
    <h1>Interactive<br><span>Learning Apps</span></h1>
    <p>Fitzwilliam Institute · Deepak John Reji · 2026</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📚 Select an App from the sidebar — or browse below")
st.markdown("<br>", unsafe_allow_html=True)

# ── App cards ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="app-card">
        <div class="icon">🎲</div>
        <div class="lecture-tag">Lecture 4 · April 16</div>
        <h3>Probability & Distributions</h3>
        <p>Probability basics, compound events, Bernoulli & Binomial distributions,
        the Normal distribution, Z-scores, and the Central Limit Theorem.
        Includes an interactive coin-flip simulator and CLT explorer.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="app-card">
        <div class="icon">🔬</div>
        <div class="lecture-tag">Lecture 7 · April 23</div>
        <h3>Two-Sample Tests & Goodness of Fit</h3>
        <p>Fisher's F-test for variance equality, independent & paired t-tests,
        Chi-square goodness-of-fit. Full worked example using the mtcars dataset
        with decision-tree walkthrough.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="app-card">
        <div class="icon">📐</div>
        <div class="lecture-tag">Lecture 6 · April 21</div>
        <h3>Confidence Intervals & Hypothesis Testing</h3>
        <p>Statistical inference, Z vs t distributions, building confidence intervals,
        hypothesis testing framework, Type I & II errors, and a fully interactive
        worked example with live visualisation.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="app-card">
        <div class="icon">🎮</div>
        <div class="lecture-tag">Lecture 8 · Multiple Linear Regression</div>
        <h3>MLR Quest — Gamified Learning</h3>
        <p>A game-style course on Multiple Linear Regression. Earn XP, unlock badges,
        and work through regression basics, assumptions, multicollinearity, one-hot
        encoding, diagnostics, and a final challenge.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Use the **sidebar** to navigate between apps. Each app is self-contained and interactive.")
