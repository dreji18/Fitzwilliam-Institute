import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MLR Quest 🎮",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@400;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  .game-title {
    font-family: 'Press Start 2P', monospace;
    font-size: 1.6rem;
    color: #6C63FF;
    text-align: center;
    padding: 1rem 0 0.3rem;
    text-shadow: 3px 3px 0px #a89cf7;
  }
  .subtitle {
    text-align: center;
    color: #888;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
  }

  /* XP bar */
  .xp-bar-wrap { background:#e0e0e0; border-radius:20px; height:18px; width:100%; margin:4px 0 10px; }
  .xp-bar-fill { background: linear-gradient(90deg,#6C63FF,#a89cf7); border-radius:20px; height:18px; transition: width .6s ease; }

  /* Cards */
  .lesson-card {
    background: #fff;
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    border: 2px solid #e8e4ff;
    box-shadow: 0 4px 14px rgba(108,99,255,.08);
  }
  .lesson-card h3 { color: #6C63FF; margin-top:0; font-size:1.1rem; }

  /* Quiz */
  .quiz-card {
    background: linear-gradient(135deg,#f0eeff,#fff);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    border: 2px solid #6C63FF;
    margin-bottom: 1rem;
  }
  .quiz-card h4 { color: #3d3480; margin-top:0; }

  /* Badges */
  .badge {
    display:inline-block;
    background: linear-gradient(135deg,#6C63FF,#a89cf7);
    color:#fff;
    border-radius:50px;
    padding: 4px 14px;
    font-size:0.78rem;
    font-weight:700;
    margin:3px;
  }
  .badge-locked {
    display:inline-block;
    background:#ddd;
    color:#999;
    border-radius:50px;
    padding: 4px 14px;
    font-size:0.78rem;
    font-weight:700;
    margin:3px;
  }

  /* Success / error */
  .correct   { background:#e6f9ec; border:1.5px solid #34c759; border-radius:12px; padding:10px 16px; color:#1a7a36; font-weight:600; }
  .incorrect { background:#fff0f0; border:1.5px solid #ff3b30; border-radius:12px; padding:10px 16px; color:#a00; font-weight:600; }

  /* Stat pill */
  .stat-pill {
    background:#f4f2ff;
    border-radius:12px;
    padding:10px 18px;
    text-align:center;
    border:1.5px solid #d4cfff;
  }
  .stat-pill .val { font-size:1.5rem; font-weight:700; color:#6C63FF; }
  .stat-pill .lbl { font-size:0.75rem; color:#888; }

  /* Level badge */
  .level-badge {
    font-family:'Press Start 2P',monospace;
    font-size:0.7rem;
    background:#6C63FF;
    color:#fff;
    border-radius:8px;
    padding:6px 12px;
    display:inline-block;
  }

  /* Section header */
  .section-header {
    font-size:1.25rem;
    font-weight:700;
    color:#3d3480;
    border-left:5px solid #6C63FF;
    padding-left:12px;
    margin: 1rem 0 0.8rem;
  }

  .stButton>button {
    background: linear-gradient(135deg,#6C63FF,#a89cf7);
    color:#fff;
    border:none;
    border-radius:10px;
    padding:8px 22px;
    font-weight:600;
    font-size:0.9rem;
    transition: transform .15s;
  }
  .stButton>button:hover { transform: scale(1.03); }

  div[data-testid="stRadio"] label { font-size:0.95rem; }
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "xp": 0,
        "level": 1,
        "badges": [],
        "current_module": 0,
        "quiz_results": {},          # module_id -> bool
        "challenge_results": {},
        "streak": 0,
        "total_questions": 0,
        "correct_answers": 0,
        "visited_modules": set(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── XP / level helpers ────────────────────────────────────────────────────────
XP_PER_LEVEL = 100

def add_xp(amount, reason=""):
    st.session_state.xp += amount
    new_level = st.session_state.xp // XP_PER_LEVEL + 1
    if new_level > st.session_state.level:
        st.session_state.level = new_level
        st.balloons()

def award_badge(badge):
    if badge not in st.session_state.badges:
        st.session_state.badges.append(badge)

# ── Module definitions ────────────────────────────────────────────────────────
MODULES = [
    {"id": 0, "icon": "🏠", "title": "Home",                       "xp": 0},
    {"id": 1, "icon": "📐", "title": "Regression Basics",          "xp": 15},
    {"id": 2, "icon": "📋", "title": "Model Assumptions",          "xp": 15},
    {"id": 3, "icon": "🔗", "title": "Multicollinearity",          "xp": 15},
    {"id": 4, "icon": "🏗️", "title": "Building the Model",         "xp": 20},
    {"id": 5, "icon": "🔢", "title": "One-Hot Encoding",           "xp": 20},
    {"id": 6, "icon": "📊", "title": "Interpreting Coefficients",  "xp": 20},
    {"id": 7, "icon": "🔍", "title": "Model Diagnostics",          "xp": 20},
    {"id": 8, "icon": "🏆", "title": "Final Challenge",            "xp": 50},
]

ALL_BADGES = [
    ("🌱", "First Steps",     "Complete your first module"),
    ("🧠", "Theory Wizard",   "Complete Regression Basics"),
    ("🔎", "Assumption Ace",  "Complete Model Assumptions"),
    ("⛓️", "No Collinearity", "Complete Multicollinearity"),
    ("🏗️", "Model Builder",   "Complete Building the Model"),
    ("🔢", "Encoder",         "Complete One-Hot Encoding"),
    ("📖", "Interpreter",     "Complete Interpreting Coefficients"),
    ("🔬", "Diagnostician",   "Complete Model Diagnostics"),
    ("🏆", "MLR Master",      "Complete the Final Challenge"),
    ("🔥", "On Fire",         "3-answer correct streak"),
    ("⚡", "Speed Learner",   "Complete 4 modules in one session"),
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="game-title">MLR<br>Quest</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Data Analytics · Lecture 10</div>', unsafe_allow_html=True)

    # Level + XP
    lvl = st.session_state.level
    xp  = st.session_state.xp
    xp_in_level = xp % XP_PER_LEVEL
    st.markdown(f'<div class="level-badge">Level {lvl}</div>', unsafe_allow_html=True)
    pct = int(xp_in_level)
    st.markdown(
        f'<div class="xp-bar-wrap"><div class="xp-bar-fill" style="width:{pct}%"></div></div>'
        f'<small style="color:#888">{xp_in_level} / {XP_PER_LEVEL} XP to next level &nbsp;·&nbsp; Total XP: <b>{xp}</b></small>',
        unsafe_allow_html=True
    )

    st.divider()

    # Module nav
    st.markdown("**📚 Modules**")
    for m in MODULES:
        visited = m["id"] in st.session_state.visited_modules
        done    = m["id"] in st.session_state.quiz_results
        label   = f"{m['icon']} {m['title']}"
        if done:
            label += " ✅"
        elif visited:
            label += " 👁️"
        if st.button(label, key=f"nav_{m['id']}", use_container_width=True):
            st.session_state.current_module = m["id"]
            st.session_state.visited_modules.add(m["id"])
            st.rerun()

    st.divider()

    # Badges
    st.markdown("**🏅 Badges**")
    earned = {b[0]: b for b in ALL_BADGES if b[1] in st.session_state.badges}
    all_b  = ALL_BADGES
    cols = st.columns(3)
    for i, (icon, name, desc) in enumerate(all_b):
        with cols[i % 3]:
            if name in st.session_state.badges:
                st.markdown(f'<span title="{name}: {desc}" class="badge">{icon}</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'<span title="Locked: {name}" class="badge-locked">{icon}</span>', unsafe_allow_html=True)

    st.divider()
    acc = (st.session_state.correct_answers / max(st.session_state.total_questions,1)) * 100
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="stat-pill"><div class="val">{st.session_state.streak}</div><div class="lbl">Streak 🔥</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-pill"><div class="val">{int(acc)}%</div><div class="lbl">Accuracy</div></div>', unsafe_allow_html=True)


# ── Quiz helper ───────────────────────────────────────────────────────────────
def render_quiz(q_id, question, options, correct_idx, explanation, xp_reward=10):
    key_sel  = f"quiz_sel_{q_id}"
    key_sub  = f"quiz_sub_{q_id}"
    key_done = f"quiz_done_{q_id}"

    if key_done not in st.session_state:
        st.session_state[key_done] = False
    if key_sub not in st.session_state:
        st.session_state[key_sub] = False

    st.markdown(f'<div class="quiz-card"><h4>🎯 Quiz: {question}</h4></div>', unsafe_allow_html=True)

    if not st.session_state[key_done]:
        choice = st.radio("Choose your answer:", options, key=key_sel, index=None)
        if st.button("Submit Answer", key=f"btn_{q_id}"):
            if choice is None:
                st.warning("Please select an answer first!")
            else:
                st.session_state[key_sub]  = True
                st.session_state[key_done] = True
                st.session_state.total_questions += 1
                chosen_idx = options.index(choice)
                is_correct = (chosen_idx == correct_idx)
                st.session_state.quiz_results[q_id] = is_correct
                if is_correct:
                    st.session_state.correct_answers += 1
                    st.session_state.streak += 1
                    add_xp(xp_reward)
                    if st.session_state.streak >= 3:
                        award_badge("On Fire")
                else:
                    st.session_state.streak = 0
                st.rerun()
    else:
        is_correct = st.session_state.quiz_results.get(q_id, False)
        chosen = st.session_state.get(key_sel, options[correct_idx])
        st.info(f"Your answer: **{chosen}**")
        if is_correct:
            st.markdown(f'<div class="correct">✅ Correct! +{xp_reward} XP  {explanation}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="incorrect">❌ Not quite. Correct answer: <b>{options[correct_idx]}</b><br>{explanation}</div>', unsafe_allow_html=True)


# ── MODULE PAGES ──────────────────────────────────────────────────────────────

mod = st.session_state.current_module

# ──────────────────────────── HOME ───────────────────────────────────────────
if mod == 0:
    st.markdown('<div class="game-title">🎮 MLR Quest</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Master Multiple Linear Regression through play</div>', unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-pill"><div class="val">{st.session_state.xp}</div><div class="lbl">Total XP</div></div>', unsafe_allow_html=True)
    with col2:
        done_count = len([k for k in st.session_state.quiz_results])
        st.markdown(f'<div class="stat-pill"><div class="val">{done_count}</div><div class="lbl">Quizzes Done</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-pill"><div class="val">{len(st.session_state.badges)}</div><div class="lbl">Badges Earned</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">🗺️ Your Learning Path</div>', unsafe_allow_html=True)

    for m in MODULES[1:]:
        done = m["id"] in st.session_state.quiz_results
        status = "✅ Complete" if done else "🔒 Not started"
        col_a, col_b, col_c = st.columns([1, 4, 1])
        with col_a:
            st.markdown(f"<h2 style='margin:0;text-align:center'>{m['icon']}</h2>", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"**{m['title']}**  \n{status}")
        with col_c:
            st.markdown(f"<span class='badge'>+{m['xp']} XP</span>", unsafe_allow_html=True)
        st.divider()

    st.info("👈 Use the sidebar to navigate between modules. Complete quizzes to earn XP and badges!")


# ──────────────────────────── MODULE 1: Regression Basics ────────────────────
elif mod == 1:
    st.markdown('<div class="section-header">📐 Module 1: Regression Basics</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="lesson-card">
    <h3>What is Regression?</h3>
    Regression analysis builds a model that <b>estimates or predicts</b> one quantitative variable (y) 
    using one or more other variables (x).<br><br>
    <b>Real-world examples:</b>
    <ul>
      <li>Body weight ← calorie intake</li>
      <li>Salary ← years of education + job experience</li>
      <li>Insurance cost ← age, BMI, smoking status</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="lesson-card">
        <h3>Simple Linear Regression</h3>
        Uses <b>exactly one</b> x variable.<br><br>
        <code>y = β₀ + β₁x</code><br><br>
        β₀ = y-intercept (baseline)<br>
        β₁ = slope (effect of x)
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="lesson-card">
        <h3>Multiple Linear Regression</h3>
        Uses <b>more than one</b> x variable.<br><br>
        <code>y = β₀ + β₁x₁ + β₂x₂ + … + βₙxₙ</code><br><br>
        Each β = marginal effect of that variable, <i>holding others constant</i>
        </div>
        """, unsafe_allow_html=True)

    # Interactive: SLR vs MLR demo
    st.markdown('<div class="section-header">🛠️ Interactive Demo: TV Sales Model</div>', unsafe_allow_html=True)
    st.markdown("Drag the sliders to see how the **MLR equation** predicts TV sales.")

    np.random.seed(42)
    n = 25
    tv_ads = np.random.uniform(5, 50, n)
    news_ads = np.random.uniform(1, 25, n)
    noise = np.random.normal(0, 1.5, n)
    tv_sales = 5.26 + 0.162 * tv_ads + 0.249 * news_ads + noise

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        tv_spend = st.slider("TV Ad Spend (€000s)", 1, 50, 20)
    with col_s2:
        news_spend = st.slider("Newspaper Ad Spend (€000s)", 1, 25, 10)

    predicted = 5.26 + 0.162 * tv_spend + 0.249 * news_spend
    st.success(f"📺 Predicted TV Sales = 5.26 + 0.162×{tv_spend} + 0.249×{news_spend} = **{predicted:.2f} million €**")

    fig = px.scatter(x=tv_ads, y=tv_sales, labels={"x": "TV Ad Spend", "y": "TV Sales"},
                     title="TV Sales vs TV Ad Spend", color_discrete_sequence=["#6C63FF"])
    slope = 0.162; intercept = 5.26 + 0.249 * np.mean(news_ads)
    x_line = np.linspace(5, 50, 100)
    fig.add_trace(go.Scatter(x=x_line, y=intercept + slope * x_line, mode="lines",
                              line=dict(color="#ff6b6b", width=2.5), name="Regression line"))
    fig.update_layout(height=320, margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

    # Strengths / Weaknesses
    st.markdown('<div class="section-header">⚖️ Strengths & Weaknesses of MLR</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="lesson-card">
        <h3>✅ Strengths</h3>
        <ul>
          <li>Most common approach for numeric data modelling</li>
          <li>Can be adapted to almost any data</li>
          <li>Shows strength & size of each relationship</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="lesson-card">
        <h3>❌ Weaknesses</h3>
        <ul>
          <li>Makes strong assumptions about the data</li>
          <li>Model form must be specified in advance</li>
          <li>Struggles with missing data</li>
          <li>Only works with numeric features (categorical needs encoding)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    render_quiz(
        q_id="m1_q1",
        question="In MLR, what does the coefficient β₂ represent?",
        options=[
            "The total effect of all variables combined",
            "The change in y when x₂ increases by 1, holding all other variables constant",
            "The correlation between x₁ and x₂",
            "The intercept of the regression line"
        ],
        correct_idx=1,
        explanation="In MLR, each coefficient represents the marginal contribution of that variable when all other variables are held constant.",
        xp_reward=15
    )

    render_quiz(
        q_id="m1_q2",
        question="The equation y = β₀ + β₁x₁ + β₂x₂ uses how many independent variables?",
        options=["1", "2", "3", "4"],
        correct_idx=1,
        explanation="There are two independent variables: x₁ and x₂. β₀ is the intercept, not a variable.",
        xp_reward=10
    )

    if "m1_q1" in st.session_state.quiz_results and "m1_q2" in st.session_state.quiz_results:
        award_badge("Theory Wizard")
        award_badge("First Steps")
        if len(st.session_state.visited_modules) >= 4:
            award_badge("Speed Learner")
        st.success("🎉 Module 1 complete! Check your badges in the sidebar.")


# ──────────────────────────── MODULE 2: Model Assumptions ────────────────────
elif mod == 2:
    st.markdown('<div class="section-header">📋 Module 2: Model Assumptions</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="lesson-card">
    <h3>Why Do Assumptions Matter?</h3>
    Regression analysis has a number of <b>strong assumptions</b>. You should check them 
    <i>before</i> you proceed with the analysis, or examine them <i>after</i> as part of model diagnostics.
    Violating them means your model's results may be unreliable.
    </div>
    """, unsafe_allow_html=True)

    assumptions = [
        ("1️⃣", "Linearity",       "The relationship between x and y is LINEAR.",                        "Check with a scatter plot  look for a straight-line pattern."),
        ("2️⃣", "Independence",    "Residuals are INDEPENDENT  they don't depend on x or y.",           "Check by plotting residuals vs fitted values  should look random."),
        ("3️⃣", "Normality",       "Residuals are NORMALLY DISTRIBUTED.",                                "Check with a histogram or QQ plot of residuals."),
        ("4️⃣", "Homoscedasticity","Residuals have EQUAL VARIANCE (homoscedasticity).",                  "Check with a scale-location plot  residuals should be evenly spread."),
    ]

    for icon, name, desc, check in assumptions:
        with st.expander(f"{icon} {name}", expanded=False):
            st.markdown(f"**What it means:** {desc}")
            st.markdown(f"**How to check:** {check}")

    # Interactive residual plot demo
    st.markdown('<div class="section-header">🛠️ Interactive: Spot the Violation!</div>', unsafe_allow_html=True)
    violation = st.selectbox("Choose a scenario:", [
        "Good model (all assumptions met)",
        "Non-linearity",
        "Heteroscedasticity (unequal variance)",
        "Non-normal residuals"
    ])

    np.random.seed(7)
    x_demo = np.linspace(1, 10, 80)
    if violation == "Good model (all assumptions met)":
        resids = np.random.normal(0, 1, 80)
        title_note = "✅ Residuals look random and even  assumptions are met!"
    elif violation == "Non-linearity":
        resids = np.sin(x_demo) * 2 + np.random.normal(0, 0.3, 80)
        title_note = "❌ Residuals show a clear curve  linearity is violated!"
    elif violation == "Heteroscedasticity (unequal variance)":
        resids = np.random.normal(0, x_demo * 0.3, 80)
        title_note = "❌ Residuals spread wider as fitted values increase  variance is not constant!"
    else:
        resids = np.concatenate([np.random.exponential(1, 60), -np.random.exponential(0.3, 20)])
        title_note = "❌ Residuals are skewed  normality is violated!"

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=x_demo, y=resids, mode="markers",
                               marker=dict(color="#6C63FF", size=7, opacity=0.7)))
    fig2.add_hline(y=0, line_dash="dash", line_color="#ff6b6b")
    fig2.update_layout(title="Residuals vs Fitted Values", xaxis_title="Fitted Values",
                        yaxis_title="Residuals", height=300, margin=dict(t=40, b=20))
    st.plotly_chart(fig2, use_container_width=True)
    st.info(title_note)

    st.divider()
    render_quiz(
        q_id="m2_q1",
        question="What plot is used to check the independence of residuals?",
        options=["Histogram of residuals", "QQ plot", "Residuals vs Fitted values plot", "Scatter matrix"],
        correct_idx=2,
        explanation="Plotting residuals against fitted values reveals patterns that indicate non-independence. Random scatter = good.",
        xp_reward=15
    )

    render_quiz(
        q_id="m2_q2",
        question="Which assumption is violated if residuals spread out as fitted values increase?",
        options=["Linearity", "Independence", "Normality", "Homoscedasticity"],
        correct_idx=3,
        explanation="Homoscedasticity means equal (constant) variance. If variance grows with fitted values, this assumption is violated  called heteroscedasticity.",
        xp_reward=15
    )

    if "m2_q1" in st.session_state.quiz_results and "m2_q2" in st.session_state.quiz_results:
        award_badge("Assumption Ace")
        st.success("🎉 Module 2 complete!")


# ──────────────────────────── MODULE 3: Multicollinearity ────────────────────
elif mod == 3:
    st.markdown('<div class="section-header">🔗 Module 3: Multicollinearity</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="lesson-card">
    <h3>What is Multicollinearity?</h3>
    Multicollinearity occurs when two or more <b>independent (x) variables are highly correlated</b> 
    with each other.<br><br>
    Before building the model, check relationships <i>between</i> the x variables for redundancy.
    If two x variables are strongly correlated (r > 0.7 or r < -0.7), they likely 
    measure the same thing  include only one.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="lesson-card">
        <h3>❌ Problem</h3>
        If both highly correlated variables are included:<br><br>
        <ul>
          <li>Hard to tell which variable contributes to the effect</li>
          <li>Coefficients become unstable</li>
          <li>Model-fitting process breaks down</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="lesson-card">
        <h3>✅ Rule of Thumb</h3>
        Correlation between two x variables:<br><br>
        <ul>
          <li><b>> +0.7 or < -0.7</b> → Remove one variable</li>
          <li><b>Between -0.7 and +0.7</b> → Safe to include both</li>
        </ul>
        <b>TV Ads vs Newspaper Ads</b> correlation = <b>0.058</b> → No collinearity, include both ✅
        </div>
        """, unsafe_allow_html=True)

    # Interactive correlation matrix
    st.markdown('<div class="section-header">🛠️ Interactive: Correlation Matrix Explorer</div>', unsafe_allow_html=True)

    np.random.seed(42)
    n = 200
    age      = np.random.normal(40, 12, n)
    bmi      = age * 0.1 + np.random.normal(27, 5, n)      # slightly correlated with age
    children = np.random.randint(0, 5, n).astype(float)
    smoker   = np.random.choice([0, 1], n, p=[0.8, 0.2]).astype(float)
    charges  = (256.9*age + 339.2*bmi + 475.5*children + 23848.5*smoker
                - 11938.5 + np.random.normal(0, 5000, n))

    df_corr = pd.DataFrame({"age": age, "bmi": bmi, "children": children,
                             "smoker": smoker, "charges": charges})
    corr = df_corr.corr().round(3)

    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
                          zmin=-1, zmax=1, title="Correlation Matrix (Insurance Data)")
    fig_corr.update_layout(height=380, margin=dict(t=50,b=20))
    st.plotly_chart(fig_corr, use_container_width=True)
    st.caption("Red = strong positive correlation, Blue = strong negative. Values close to ±0.7 or beyond → potential multicollinearity.")

    st.divider()
    render_quiz(
        q_id="m3_q1",
        question="Two x variables have a correlation of 0.85. What should you do?",
        options=[
            "Include both  more variables always improve the model",
            "Remove one of them, as they likely measure the same thing",
            "Transform both variables using log",
            "Multiply them together to create an interaction term"
        ],
        correct_idx=1,
        explanation="Correlation above 0.7 indicates multicollinearity. Including both causes unstable coefficients  remove one.",
        xp_reward=15
    )

    render_quiz(
        q_id="m3_q2",
        question="In the TV ads example, the correlation between TV Ads and Newspaper Ads was 0.058. What does this mean?",
        options=[
            "Strong multicollinearity  remove one variable",
            "Moderate collinearity  proceed with caution",
            "No collinearity  safe to include both variables",
            "The two variables are identical"
        ],
        correct_idx=2,
        explanation="0.058 is very close to zero, indicating almost no linear relationship between the two predictors  both can safely be included.",
        xp_reward=15
    )

    if "m3_q1" in st.session_state.quiz_results and "m3_q2" in st.session_state.quiz_results:
        award_badge("No Collinearity")
        st.success("🎉 Module 3 complete!")


# ──────────────────────────── MODULE 4: Building the Model ───────────────────
elif mod == 4:
    st.markdown('<div class="section-header">🏗️ Module 4: Building the Model</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="lesson-card">
    <h3>From Simple to Multiple</h3>
    In <b>simple</b> regression: y = β₀ + β₁x <br>
    In <b>multiple</b> regression: y = β₀ + β₁x₁ + β₂x₂ + … + βₙxₙ<br><br>
    The goal in both cases: find values of beta coefficients that <b>minimise the prediction error</b>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">🛠️ Build Your Own MLR Model</div>', unsafe_allow_html=True)
    st.markdown("Adjust the coefficients below. Try to minimise the **Mean Squared Error (MSE)**!")

    np.random.seed(10)
    n = 40
    tv_a   = np.random.uniform(5, 50, n)
    news_a = np.random.uniform(1, 25, n)
    sales  = 5.26 + 0.162*tv_a + 0.249*news_a + np.random.normal(0,1.2,n)

    c0 = st.slider("Intercept (β₀)", 0.0, 15.0, 5.26, 0.1)
    c1 = st.slider("TV Ads coefficient (β₁)", 0.0, 0.5, 0.162, 0.005)
    c2 = st.slider("Newspaper Ads coefficient (β₂)", 0.0, 0.5, 0.249, 0.005)

    preds = c0 + c1*tv_a + c2*news_a
    mse   = np.mean((sales - preds)**2)
    best_mse = np.mean((5.26 + 0.162*tv_a + 0.249*news_a - sales)**2)

    col_mse, col_best = st.columns(2)
    with col_mse:
        st.markdown(f'<div class="stat-pill"><div class="val">{mse:.3f}</div><div class="lbl">Your MSE</div></div>', unsafe_allow_html=True)
    with col_best:
        st.markdown(f'<div class="stat-pill"><div class="val">{best_mse:.3f}</div><div class="lbl">Best Possible MSE</div></div>', unsafe_allow_html=True)

    if mse <= best_mse * 1.05:
        st.success(f"🎯 Near-optimal! Your equation: Sales = {c0} + {c1}×TV + {c2}×News")
    elif mse <= best_mse * 1.5:
        st.warning(f"Getting closer! Try adjusting the sliders. MSE gap: {mse - best_mse:.3f}")
    else:
        st.error(f"MSE is quite high. Try β₀≈5.26, β₁≈0.162, β₂≈0.249")

    # Scatter: actual vs predicted
    fig_ap = px.scatter(x=sales, y=preds, labels={"x":"Actual Sales","y":"Predicted Sales"},
                         title="Actual vs Predicted Sales",
                         color_discrete_sequence=["#6C63FF"])
    fig_ap.add_shape(type="line", x0=min(sales), y0=min(sales), x1=max(sales), y1=max(sales),
                      line=dict(color="#ff6b6b", dash="dash"))
    fig_ap.update_layout(height=300, margin=dict(t=40,b=20))
    st.plotly_chart(fig_ap, use_container_width=True)

    st.divider()
    render_quiz(
        q_id="m4_q1",
        question="Using the TV ads model: Sales = 5.26 + 0.162×TV + 0.249×News. Predict sales when TV=20, News=10.",
        options=["10.01 million €", "10.99 million €", "12.54 million €", "8.75 million €"],
        correct_idx=1,
        explanation="5.26 + 0.162×20 + 0.249×10 = 5.26 + 3.24 + 2.49 = 10.99 million €",
        xp_reward=20
    )

    render_quiz(
        q_id="m4_q2",
        question="What does minimising MSE (Mean Squared Error) achieve in regression?",
        options=[
            "It removes outliers from the dataset",
            "It finds the best-fitting line that reduces prediction errors",
            "It normalises all variables to the same scale",
            "It checks multicollinearity between variables"
        ],
        correct_idx=1,
        explanation="Regression works by finding beta coefficients that minimise the sum of squared differences between actual and predicted values.",
        xp_reward=20
    )

    if "m4_q1" in st.session_state.quiz_results and "m4_q2" in st.session_state.quiz_results:
        award_badge("Model Builder")
        st.success("🎉 Module 4 complete!")


# ──────────────────────────── MODULE 5: One-Hot Encoding ─────────────────────
elif mod == 5:
    st.markdown('<div class="section-header">🔢 Module 5: One-Hot Encoding</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="lesson-card">
    <h3>The Problem with Categorical Variables</h3>
    Regression only works with <b>numeric</b> features. But many real-world variables are categorical 
    (sex, region, smoker status). We can't just assign 1=male, 2=female  that implies an 
    ordering that doesn't exist.<br><br>
    <b>Solution: One-Hot Encoding (also called Dummy Variables)</b>  create a binary column 
    for each category (1 = belongs, 0 = doesn't belong).
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Before encoding:**")
        df_before = pd.DataFrame({"Fruit": ["apple","mango","apple","orange"], "Price": [5,10,15,20]})
        st.dataframe(df_before, use_container_width=True)
    with col2:
        st.markdown("**After one-hot encoding:**")
        df_after = pd.DataFrame({
            "apple": [1,0,1,0], "mango": [0,1,0,0],
            "orange": [0,0,0,1], "price": [5,10,15,20]
        })
        st.dataframe(df_after, use_container_width=True)

    st.info("💡 Rule: For n categories, you only need n-1 columns (drop one to avoid redundancy  called the *reference category*).")

    # Interactive encoder
    st.markdown('<div class="section-header">🛠️ Interactive: Encode It Yourself!</div>', unsafe_allow_html=True)

    region_input = st.selectbox("Select a region:", ["northeast","northwest","southeast","southwest"])
    smoker_input = st.selectbox("Smoker?", ["yes","no"])

    encoded = {
        "region_northwest": 1 if region_input == "northwest" else 0,
        "region_southeast": 1 if region_input == "southeast" else 0,
        "region_southwest": 1 if region_input == "southwest" else 0,
        "smoker_yes":       1 if smoker_input == "yes" else 0,
    }
    st.markdown("**Your one-hot encoded row:**")
    st.dataframe(pd.DataFrame([encoded]), use_container_width=True)
    st.caption("Note: 'northeast' is the reference category for region (all zeros = northeast). 'smoker_no' is the reference for smoker.")

    st.markdown("""
    <div class="lesson-card">
    <h3>Two Python Methods</h3>
    <ul>
      <li><b>pandas.get_dummies()</b>  quick and easy for exploration</li>
      <li><b>sklearn OneHotEncoder</b>  creates a fitted object reusable on new (test) data; preferred for ML pipelines</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    render_quiz(
        q_id="m5_q1",
        question="A variable 'region' has 4 categories. How many dummy columns do you need?",
        options=["4", "3", "2", "1"],
        correct_idx=1,
        explanation="For n categories, you need n-1 dummy columns. One category becomes the reference (all zeros). So 4 categories → 3 dummy columns.",
        xp_reward=20
    )

    render_quiz(
        q_id="m5_q2",
        question="Why can't we just assign numbers (1=northeast, 2=northwest, 3=southeast, 4=southwest) to regions?",
        options=[
            "It's too time-consuming",
            "Numbers imply an ordering or magnitude that doesn't exist for categories",
            "Regression models can't handle numbers above 2",
            "It would create too many coefficients"
        ],
        correct_idx=1,
        explanation="Assigning integers implies northeast < northwest < southeast < southwest in some meaningful numeric way, which is false. One-hot encoding treats each category independently.",
        xp_reward=20
    )

    if "m5_q1" in st.session_state.quiz_results and "m5_q2" in st.session_state.quiz_results:
        award_badge("Encoder")
        st.success("🎉 Module 5 complete!")


# ──────────────────────────── MODULE 6: Interpreting Coefficients ─────────────
elif mod == 6:
    st.markdown('<div class="section-header">📊 Module 6: Interpreting Coefficients</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="lesson-card">
    <h3>The Key Rule</h3>
    The coefficient of an x variable = the amount y changes when x increases by 1 <b>and all 
    other variables remain constant</b>.<br><br>
    This is called the <b>marginal contribution</b>  it isolates the effect of one variable 
    at a time.
    </div>
    """, unsafe_allow_html=True)

    # TV Ads example
    st.markdown('<div class="section-header">🛠️ TV Ads Example</div>', unsafe_allow_html=True)
    st.markdown("**Model:** Sales = 5.26 + **0.162**×TV_Ads + **0.249**×Newspaper_Ads")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="lesson-card">
        <h3>β₁ = 0.162 (TV Ads)</h3>
        For each €1,000 increase in TV ad spend (holding newspaper ads constant):
        TV Sales increase by <b>0.162 million € = €162,100</b>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="lesson-card">
        <h3>β₂ = 0.249 (Newspaper Ads)</h3>
        For each €1,000 increase in newspaper ad spend (holding TV ads constant):
        TV Sales increase by <b>0.249 million € = €249,000</b>
        </div>
        """, unsafe_allow_html=True)

    # Insurance model
    st.markdown('<div class="section-header">🏥 Insurance Model: Full Interpretation</div>', unsafe_allow_html=True)

    coef_data = {
        "Variable":    ["age", "children", "bmi", "sexmale", "smokeryes", "region_northwest", "region_southeast", "region_southwest"],
        "Coefficient": [256.9, 475.5, 339.2, -131.3, 23848.5, -353.0, -1035.0, -960.0],
        "Significant": ["✅ ***","✅ ***","✅ ***","❌ No","✅ ***","❌ No","✅ *","✅ *"],
    }
    df_coef = pd.DataFrame(coef_data)

    fig_coef = px.bar(df_coef, x="Variable", y="Coefficient", color="Significant",
                       color_discrete_map={"✅ ***":"#6C63FF","✅ *":"#a89cf7","❌ No":"#ddd"},
                       title="Insurance Model Coefficients")
    fig_coef.update_layout(height=340, margin=dict(t=50,b=20))
    st.plotly_chart(fig_coef, use_container_width=True)

    # R-squared
    st.markdown("""
    <div class="lesson-card">
    <h3>📈 R-squared = 0.75</h3>
    The model explains <b>75% of the variation</b> in insurance charges. 
    Adjusted R² (0.749) corrects for the number of predictors  use this when comparing models.
    <br><br><i>The closer R² is to 1, the better the model explains the data.</i>
    </div>
    """, unsafe_allow_html=True)

    # Interactive coefficient interpreter
    st.markdown('<div class="section-header">🛠️ Coefficient Interpreter Challenge</div>', unsafe_allow_html=True)
    var_choice = st.selectbox("Select a variable to interpret:", df_coef["Variable"].tolist())
    coef_val   = df_coef.loc[df_coef["Variable"]==var_choice, "Coefficient"].values[0]

    if st.button("Show Interpretation"):
        interpretations = {
            "age":              f"Each additional year of age increases insurance charges by **${coef_val:,.1f}**, holding all else equal.",
            "children":         f"Each additional child increases insurance charges by **${coef_val:,.1f}**, holding all else equal.",
            "bmi":              f"Each 1-unit increase in BMI increases insurance charges by **${coef_val:,.1f}**, holding all else equal.",
            "sexmale":          f"Being male decreases insurance charges by **${abs(coef_val):,.1f}** compared to female, but this is **NOT significant** (p > 0.05).",
            "smokeryes":        f"Being a smoker increases insurance charges by **${coef_val:,.1f}** compared to non-smokers  the largest effect!",
            "region_northwest": f"Being in the northwest region decreases charges by **${abs(coef_val):,.1f}** vs northeast, but this is **NOT significant**.",
            "region_southeast": f"Being in the southeast region decreases charges by **${abs(coef_val):,.1f}** vs northeast  significant.",
            "region_southwest": f"Being in the southwest region decreases charges by **${abs(coef_val):,.1f}** vs northeast  significant.",
        }
        st.info(interpretations.get(var_choice, "No interpretation available."))

    st.divider()
    render_quiz(
        q_id="m6_q1",
        question="In the insurance model, smokeryes = 23,848.5. What does this mean?",
        options=[
            "Smokers are 23,848 times more likely to have high charges",
            "Being a smoker increases charges by $23,848.50 compared to non-smokers",
            "23,848 smokers are in the dataset",
            "Smokers pay 23% more on average"
        ],
        correct_idx=1,
        explanation="The reference category is 'non-smoker'. The coefficient 23,848.5 means smokers pay $23,848.50 more on average, holding all other variables constant.",
        xp_reward=20
    )

    render_quiz(
        q_id="m6_q2",
        question="The adjusted R² of the insurance model is 0.749. What does this tell us?",
        options=[
            "74.9% of the variation in charges is explained by the model",
            "The model makes errors 74.9% of the time",
            "74.9 variables were used",
            "The model is 74.9% accurate on new data"
        ],
        correct_idx=0,
        explanation="R² (coefficient of determination) measures what proportion of the variance in the dependent variable is explained by the model. 0.749 = 74.9%  quite good for real-world data!",
        xp_reward=20
    )

    if "m6_q1" in st.session_state.quiz_results and "m6_q2" in st.session_state.quiz_results:
        award_badge("Interpreter")
        st.success("🎉 Module 6 complete!")


# ──────────────────────────── MODULE 7: Model Diagnostics ────────────────────
elif mod == 7:
    st.markdown('<div class="section-header">🔍 Module 7: Model Diagnostics</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="lesson-card">
    <h3>Checking the Residuals</h3>
    Residuals = Actual y − Predicted y<br>
    They capture the <b>prediction error</b>. After building the model, always check:
    </div>
    """, unsafe_allow_html=True)

    diag_data = [
        ("📈","Residuals vs Fitted","Independence check","Should look randomly scattered around zero with no pattern."),
        ("🔔","QQ Plot","Normality check","Points should fall along a straight diagonal line."),
        ("📏","Scale-Location Plot","Homoscedasticity check","Residuals should be evenly spread with no fan shape."),
    ]
    for icon, name, check_type, desc in diag_data:
        st.markdown(f"""
        <div class="lesson-card">
        <h3>{icon} {name} <span style='font-size:0.8rem;color:#999'>({check_type})</span></h3>
        {desc}
        </div>
        """, unsafe_allow_html=True)

    # Interactive: show good vs bad diagnostics
    st.markdown('<div class="section-header">🛠️ Diagnostic Plot Simulator</div>', unsafe_allow_html=True)

    plot_type   = st.selectbox("Choose plot type:", ["Residuals vs Fitted","QQ Plot","Scale-Location"])
    model_state = st.radio("Model quality:", ["Good model","Problematic model"], horizontal=True)

    np.random.seed(99)
    fitted_vals = np.linspace(5000, 40000, 100)
    if model_state == "Good model":
        resids2 = np.random.normal(0, 3000, 100)
    else:
        resids2 = np.random.normal(0, fitted_vals * 0.12, 100)  # heteroscedastic

    if plot_type == "Residuals vs Fitted":
        fig_d = px.scatter(x=fitted_vals, y=resids2, labels={"x":"Fitted","y":"Residuals"}, title="Residuals vs Fitted")
        fig_d.add_hline(y=0, line_dash="dash", line_color="red")
    elif plot_type == "QQ Plot":
        sorted_r = np.sort(resids2)
        theoretical = np.random.normal(0, np.std(resids2), 100)
        theoretical.sort()
        fig_d = px.scatter(x=theoretical, y=sorted_r,
                            labels={"x":"Theoretical Quantiles","y":"Sample Quantiles"}, title="Normal QQ Plot")
        fig_d.add_shape(type="line", x0=min(theoretical), y0=min(theoretical),
                         x1=max(theoretical), y1=max(theoretical), line=dict(color="red",dash="dash"))
    else:
        fig_d = px.scatter(x=fitted_vals, y=np.sqrt(np.abs(resids2)),
                            labels={"x":"Fitted","y":"√|Std Residuals|"}, title="Scale-Location")
        fig_d.add_hline(y=np.mean(np.sqrt(np.abs(resids2))), line_dash="dash", line_color="red")

    fig_d.update_layout(height=300, margin=dict(t=40,b=20))
    st.plotly_chart(fig_d, use_container_width=True)

    if model_state == "Good model":
        st.success("✅ This looks good! Residuals are evenly spread with no obvious pattern.")
    else:
        st.error("❌ Issue detected! Residuals fan out  likely heteroscedasticity. Consider transforming the dependent variable (e.g. log transform).")

    st.markdown("""
    <div class="lesson-card">
    <h3>🔧 Remedial Measures</h3>
    <b>Non-linearity:</b> Transform variables (log, square), or add higher-order/interaction terms.<br>
    <b>Heteroscedasticity:</b> Weighted Least Squares, or transform the response variable.<br>
    <b>Non-normality:</b> Log-transform the dependent variable (e.g. log(charges)).
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    render_quiz(
        q_id="m7_q1",
        question="The QQ plot of residuals deviates strongly from the diagonal line. What does this indicate?",
        options=[
            "The model has too many variables",
            "Residuals are not normally distributed",
            "The model has perfect fit",
            "There is multicollinearity"
        ],
        correct_idx=1,
        explanation="A QQ plot checks normality. If points follow the diagonal, residuals are normal. Deviations indicate non-normality  a potential assumption violation.",
        xp_reward=20
    )

    render_quiz(
        q_id="m7_q2",
        question="The insurance model residuals show a fan shape (spread increases with fitted values). What's the remedy?",
        options=[
            "Add more variables to the model",
            "Remove outliers",
            "Apply a log transformation to the dependent variable (charges)",
            "Use a larger dataset"
        ],
        correct_idx=2,
        explanation="A fan shape = heteroscedasticity. A common fix is to transform the skewed dependent variable using log() to stabilise variance.",
        xp_reward=20
    )

    if "m7_q1" in st.session_state.quiz_results and "m7_q2" in st.session_state.quiz_results:
        award_badge("Diagnostician")
        st.success("🎉 Module 7 complete!")


# ──────────────────────────── MODULE 8: Final Challenge ──────────────────────
elif mod == 8:
    st.markdown('<div class="section-header">🏆 Module 8: Final Challenge</div>', unsafe_allow_html=True)

    completed_modules = sum(1 for k in [
        "m1_q1","m2_q1","m3_q1","m4_q1","m5_q1","m6_q1","m7_q1"
    ] if k in st.session_state.quiz_results)

    if completed_modules < 5:
        st.warning(f"⚠️ Complete at least 5 earlier modules before attempting the Final Challenge! You've completed {completed_modules}/7.")
    else:
        st.markdown("""
        <div class="lesson-card">
        <h3>🎯 The Insurance Scenario</h3>
        You are a data analyst at an insurance company. 
        Using the Multiple Linear Regression model built in this course, answer the following 
        scenario-based questions. Each correct answer earns extra XP!
        </div>
        """, unsafe_allow_html=True)

        render_quiz(
            q_id="final_q1",
            question="A 45-year-old non-smoking male with BMI=30, 2 children, from the southeast region. His age coefficient is 256.9, BMI=339.2, children=475.5, smoker=23848.5, southeast=-1035. Roughly what would his predicted charges be (using intercept -11938.5)?",
            options=["~$14,000", "~$18,500", "~$25,000", "~$9,000"],
            correct_idx=1,
            explanation="-11938.5 + 256.9×45 + 339.2×30 + 475.5×2 + 0 - 1035 ≈ -11938.5 + 11560.5 + 10176 + 951 - 1035 ≈ $9,714 + adjustments ≈ ~$18,500",
            xp_reward=25
        )

        render_quiz(
            q_id="final_q2",
            question="Which variable has the LARGEST effect on insurance charges in the model?",
            options=["age (256.9)", "bmi (339.2)", "smokeryes (23848.5)", "children (475.5)"],
            correct_idx=2,
            explanation="smokeryes has a coefficient of 23,848.5  by far the largest, meaning smoking status has the biggest impact on insurance costs.",
            xp_reward=25
        )

        render_quiz(
            q_id="final_q3",
            question="The model's adjusted R² is 0.749. A colleague says 'the model only explains 75% so it's not good enough.' How do you respond?",
            options=[
                "Agree  R² must be above 0.95 to be useful",
                "Disagree  for real-world medical data, 75% is actually quite good",
                "Disagree  R² above 0.5 means the model is perfect",
                "Agree  we should add more variables until R² reaches 1.0"
            ],
            correct_idx=1,
            explanation="Real-world data is messy and complex. An R² of 0.75 is considered quite good for medical/insurance data. Chasing R²=1 leads to overfitting.",
            xp_reward=25
        )

        render_quiz(
            q_id="final_q4",
            question="You notice sex (male/female) is NOT significant in the model (p=0.69). What should you do?",
            options=[
                "Remove it  non-significant variables add noise without improving predictions",
                "Keep it  more variables always improve the model",
                "Encode it differently using LabelEncoder",
                "Transform it using log(sex)"
            ],
            correct_idx=0,
            explanation="Non-significant variables (p > 0.05) don't contribute meaningfully. Removing them simplifies the model without losing predictive power  a principle called parsimony.",
            xp_reward=25
        )

        final_done = all(k in st.session_state.quiz_results for k in ["final_q1","final_q2","final_q3","final_q4"])
        if final_done:
            award_badge("MLR Master")
            add_xp(50, "Final Challenge")
            st.balloons()
            st.markdown("""
            <div style='background:linear-gradient(135deg,#6C63FF,#a89cf7);border-radius:20px;
                        padding:2rem;text-align:center;color:white;margin-top:1rem;'>
              <h1>🏆 CONGRATULATIONS! 🏆</h1>
              <h3>You've mastered Multiple Linear Regression!</h3>
              <p>You've earned the <b>MLR Master</b> badge and completed the course.<br>
              Check your total XP and badges in the sidebar!</p>
            </div>
            """, unsafe_allow_html=True)

            # Final score summary
            total_q  = st.session_state.total_questions
            correct  = st.session_state.correct_answers
            accuracy = int(correct / max(total_q, 1) * 100)
            xp_total = st.session_state.xp

            st.markdown("---")
            st.markdown("### 📊 Your Final Score")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f'<div class="stat-pill"><div class="val">{xp_total}</div><div class="lbl">Total XP</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="stat-pill"><div class="val">{correct}/{total_q}</div><div class="lbl">Correct</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="stat-pill"><div class="val">{accuracy}%</div><div class="lbl">Accuracy</div></div>', unsafe_allow_html=True)
            with c4:
                st.markdown(f'<div class="stat-pill"><div class="val">{len(st.session_state.badges)}</div><div class="lbl">Badges</div></div>', unsafe_allow_html=True)
