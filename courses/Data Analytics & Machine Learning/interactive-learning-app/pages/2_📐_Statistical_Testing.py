import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
from scipy.stats import norm, t
import warnings
warnings.filterwarnings('ignore')

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Statistical Testing – Interactive Lecture",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --navy:   #0f1b2d;
    --teal:   #0d9488;
    --amber:  #f59e0b;
    --rose:   #e11d48;
    --slate:  #1e293b;
    --light:  #f0fdf9;
    --card:   #ffffff;
    --muted:  #64748b;
    --border: #e2e8f0;
}

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--navy) !important;
    border-right: 3px solid var(--teal);
}
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
section[data-testid="stSidebar"] .stRadio label {
    font-size: 14px !important;
    padding: 6px 0 !important;
}

/* Main headings */
h1 { font-family: 'Playfair Display', serif !important; color: var(--navy) !important; }
h2 { font-family: 'Playfair Display', serif !important; color: var(--slate) !important; }
h3 { font-family: 'Source Sans 3', sans-serif !important; color: var(--teal) !important; font-weight: 600 !important; }

/* Metric cards */
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 4px solid var(--teal);
    border-radius: 10px;
    padding: 18px 20px;
    margin: 8px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* Info boxes */
.info-box {
    background: #f0fdf9;
    border: 1px solid #99f6e4;
    border-left: 4px solid var(--teal);
    border-radius: 8px;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 15px;
    line-height: 1.6;
}

.warning-box {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-left: 4px solid var(--amber);
    border-radius: 8px;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 15px;
    line-height: 1.6;
}

.danger-box {
    background: #fff1f2;
    border: 1px solid #fecdd3;
    border-left: 4px solid var(--rose);
    border-radius: 8px;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 15px;
    line-height: 1.6;
}

.formula-box {
    background: var(--navy);
    color: #a5f3fc !important;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 12px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 15px;
    text-align: center;
    letter-spacing: 0.04em;
}

.step-badge {
    display: inline-block;
    background: var(--teal);
    color: white;
    border-radius: 50%;
    width: 28px;
    height: 28px;
    line-height: 28px;
    text-align: center;
    font-weight: 700;
    font-size: 13px;
    margin-right: 8px;
}

.result-reject {
    background: #fff1f2;
    border: 2px solid var(--rose);
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
    font-weight: 700;
    font-size: 17px;
    color: var(--rose);
}

.result-fail {
    background: #f0fdf9;
    border: 2px solid var(--teal);
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
    font-weight: 700;
    font-size: 17px;
    color: var(--teal);
}

/* Code styling */
code {
    background: #1e293b !important;
    color: #a5f3fc !important;
    border-radius: 4px;
    padding: 2px 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    font-family: 'Source Sans 3', sans-serif;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 Data Analytics")
    st.markdown("### Lecture 6")
    st.markdown("---")
    topic = st.radio("**Navigate**", [
        "🏠  Overview",
        "📐  Statistical Inference",
        "📏  Confidence Intervals",
        "🔬  CI in Python",
        "🧪  Hypothesis Testing",
        "⚠️  Type I & II Errors",
        "🔢  Worked Example",
        "🎮  Quiz",
    ])
    st.markdown("---")
    st.markdown("**Fitzwilliam Institute**  \nDiploma in Data Analytics")


# ═══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
if "Overview" in topic:
    st.title("Lecture 6 - Confidence Intervals & Hypothesis Testing")
    st.markdown("*April 21st, 2026 · Fitzwilliam Institute*")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### What we cover today")
        st.markdown("""
<div class="info-box">
This lecture bridges the gap between <strong>probability theory</strong> and <strong>real-world data decisions</strong>.
We learn how to make statements about populations using sample data - and attach a level of confidence to those statements.
</div>
""", unsafe_allow_html=True)

        topics_list = [
            ("📐", "Statistical Inference", "Estimation vs Hypothesis Testing"),
            ("📏", "Confidence Intervals", "What they are, how to build them"),
            ("📊", "Z & T Distributions", "When to use which"),
            ("🧪", "Hypothesis Testing", "Null & alternative hypotheses"),
            ("⚠️", "Type I & II Errors", "Significance level α & β"),
            ("🔢", "Worked Examples", "Light bulb lifetime test in Python"),
        ]
        for icon, title, desc in topics_list:
            st.markdown(f"""
<div class="metric-card">
<strong>{icon} {title}</strong><br>
<span style="color:#64748b;font-size:14px">{desc}</span>
</div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("### Useful Libraries")
        st.code("""import numpy as np
from scipy.stats import norm, t
import statsmodels.api as sm""", language="python")

        st.markdown("### Docs")
        st.markdown("""
- [NumPy Docs](https://numpy.org/doc/1.23/)
- [SciPy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)
""")

    st.markdown("---")
    st.markdown("### Recall: Central Limit Theorem")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
<div class="info-box">
<strong>🔵 Large Samples (n ≥ 30)</strong><br>
The Central Limit Theorem guarantees that the distribution of the sample mean is
<em>approximately normal</em> - even if the original population is not.
</div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown("""
<div class="warning-box">
<strong>🟡 Small Samples (n &lt; 30)</strong><br>
The sample mean is normally distributed <em>only if</em> the original population itself is normal.
Otherwise we must use the <strong>t-distribution</strong>.
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# STATISTICAL INFERENCE
# ═══════════════════════════════════════════════════════════════════════════════
elif "Inference" in topic:
    st.title("📐 Statistical Inference")
    st.markdown("*Applying probability to situations where you have data*")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 1. Estimation")
        st.markdown("""
<div class="info-box">
Use sample information to <strong>estimate</strong> population parameters such as mean, median, and variance.<br><br>
Uncertainty is captured by a <strong>Confidence Interval</strong> - a range with an associated confidence level.
</div>""", unsafe_allow_html=True)
        st.markdown("**Example →**")
        st.markdown("""
> *"44 % of those surveyed approved of the President's reaction"*  
> **Margin of error: ± 3.5 %**  
> So the true proportion lies between **40.5 %** and **47.5 %**
""")

    with col2:
        st.markdown("### 2. Statistical Test")
        st.markdown("""
<div class="info-box">
Use sample information to decide whether a <strong>claim about the population</strong> is supported by the data.<br><br>
You test whether results are real or simply occurred <em>by chance</em>.
</div>""", unsafe_allow_html=True)
        st.markdown("**Example →**")
        st.markdown("""
> The Republican Party claimed Trump's approval rating was **> 75 %** (summer 2020).  
> We use poll data to decide whether that claim is supported.
""")

    st.markdown("---")
    st.markdown("### Good Estimator Properties")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
<div class="metric-card">
<strong>① Unbiased</strong><br>
The centre of the sampling distribution equals the population mean.<br>
<code>Mean(x̄) = μ</code>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="metric-card">
<strong>② Efficient</strong><br>
Smallest standard error compared to all other estimators.<br>
<code>SE = σ / √n</code>
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Interactive: Standard Error Explorer")
    st.markdown("See how sample size affects the Standard Error of the Mean:")
    sigma_val = st.slider("Population Standard Deviation (σ)", 1, 50, 15)
    n_range = np.arange(5, 501, 5)
    se_vals = sigma_val / np.sqrt(n_range)

    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.plot(n_range, se_vals, color="#0d9488", lw=2.5)
    ax.fill_between(n_range, se_vals, alpha=0.15, color="#0d9488")
    ax.set_xlabel("Sample size (n)", fontsize=12)
    ax.set_ylabel("Standard Error", fontsize=12)
    ax.set_title(f"SE = σ/√n  (σ = {sigma_val})", fontsize=13, fontweight='bold')
    ax.axvline(30, color="#f59e0b", ls="--", lw=1.5, label="n = 30 threshold")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()
    st.markdown(f"""
<div class="info-box">
At n = 30 → SE = <strong>{sigma_val/np.sqrt(30):.3f}</strong> &nbsp;|&nbsp;
At n = 100 → SE = <strong>{sigma_val/np.sqrt(100):.3f}</strong> &nbsp;|&nbsp;
At n = 500 → SE = <strong>{sigma_val/np.sqrt(500):.3f}</strong>
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIDENCE INTERVALS (THEORY)
# ═══════════════════════════════════════════════════════════════════════════════
elif "Confidence Intervals" in topic:
    st.title("📏 Confidence Intervals")
    st.markdown("---")

    st.markdown("### What is a Confidence Interval?")
    st.markdown("""
<div class="info-box">
A <strong>Confidence Interval (CI)</strong> is a range of values, computed from sample data, that is likely
to contain the true population parameter with a specified level of confidence.<br><br>
<strong>Formula:</strong>
</div>""", unsafe_allow_html=True)

    st.markdown("""
<div class="formula-box">
CI  =  x̄  ±  (z-critical)  ×  (σ / √n)
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Common Confidence Levels & Z-Critical Values")

    ci_data = {
        "Confidence Level": ["90%", "95%", "99%"],
        "z-critical":       [1.645, 1.960, 2.576],
        "α (significance)": [0.10,  0.05,  0.01],
        "α/2 (one tail)":   [0.05,  0.025, 0.005],
    }
    col_h = st.columns(4)
    headers = list(ci_data.keys())
    for i, h in enumerate(headers):
        col_h[i].markdown(f"**{h}**")

    rows = list(zip(*ci_data.values()))
    for row in rows:
        cols = st.columns(4)
        for i, val in enumerate(row):
            cols[i].markdown(str(val))

    st.markdown("---")
    st.markdown("### 🎛️ Interactive: Build Your Own CI")

    col1, col2, col3 = st.columns(3)
    with col1:
        x_bar = st.number_input("Sample Mean (x̄)", value=172.0, step=0.5)
        sigma = st.number_input("Std Deviation (σ)", value=9.5, min_value=0.01, step=0.5)
    with col2:
        n_ci = st.number_input("Sample Size (n)", value=209, min_value=2, step=1)
        conf = st.selectbox("Confidence Level", [0.90, 0.95, 0.99], index=1,
                            format_func=lambda x: f"{int(x*100)}%")
    with col3:
        st.markdown(" ")
        z_crit_map = {0.90: 1.645, 0.95: 1.960, 0.99: 2.576}
        z_crit = z_crit_map[conf]
        se = sigma / np.sqrt(n_ci)
        moe = z_crit * se
        ci_lower = x_bar - moe
        ci_upper = x_bar + moe
        st.markdown(f"""
<div class="metric-card">
<strong>z-critical</strong>: {z_crit}<br>
<strong>Std Error (SE)</strong>: {se:.4f}<br>
<strong>Margin of Error</strong>: {moe:.4f}
</div>""", unsafe_allow_html=True)

    st.markdown(f"""
<div class="result-fail" style="font-size:16px;">
We are {int(conf*100)}% confident that the true population mean lies between
<strong>{ci_lower:.3f}</strong> and <strong>{ci_upper:.3f}</strong>
</div>""", unsafe_allow_html=True)

    # Visualisation
    fig, ax = plt.subplots(figsize=(10, 3.5))
    x_plot = np.linspace(x_bar - 5*se, x_bar + 5*se, 500)
    y_plot = norm.pdf(x_plot, x_bar, se)
    ax.plot(x_plot, y_plot, color="#0f1b2d", lw=2)

    # shade CI
    x_shade = np.linspace(ci_lower, ci_upper, 300)
    ax.fill_between(x_shade, norm.pdf(x_shade, x_bar, se), alpha=0.35, color="#0d9488", label=f"{int(conf*100)}% CI")

    # shade tails
    x_left  = np.linspace(x_bar - 5*se, ci_lower, 200)
    x_right = np.linspace(ci_upper, x_bar + 5*se, 200)
    ax.fill_between(x_left,  norm.pdf(x_left,  x_bar, se), alpha=0.4, color="#e11d48", label="Rejection region")
    ax.fill_between(x_right, norm.pdf(x_right, x_bar, se), alpha=0.4, color="#e11d48")

    ax.axvline(ci_lower, color="#e11d48", ls="--", lw=1.5, label=f"Lower: {ci_lower:.2f}")
    ax.axvline(ci_upper, color="#0d9488", ls="--", lw=1.5, label=f"Upper: {ci_upper:.2f}")
    ax.axvline(x_bar,    color="#0f1b2d", ls="-",  lw=1.5, label=f"x̄ = {x_bar}")
    ax.set_xlabel("Value", fontsize=11)
    ax.set_title(f"Sampling Distribution with {int(conf*100)}% Confidence Interval", fontsize=13, fontweight='bold')
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("---")
    st.markdown("### Large vs Small Samples")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
<div class="info-box">
<strong>Large sample (n ≥ 30)</strong><br>
Use the <strong>z-distribution</strong> (standard normal).<br>
CI formula uses <code>z-critical × SE</code>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="warning-box">
<strong>Small sample (n &lt; 30)</strong><br>
Use the <strong>t-distribution</strong> (heavier tails).<br>
CI formula uses <code>t-critical × SE</code> with <strong>df = n − 1</strong>
</div>""", unsafe_allow_html=True)

    # Z vs T comparison
    st.markdown("#### 🔍 Z-distribution vs T-distribution")
    df_val = st.slider("Degrees of freedom (df = n−1)", 2, 30, 10)
    x_comp = np.linspace(-4, 4, 500)
    fig2, ax2 = plt.subplots(figsize=(9, 3.5))
    ax2.plot(x_comp, norm.pdf(x_comp), color="#0d9488", lw=2.5, label="Z (normal)")
    ax2.plot(x_comp, t.pdf(x_comp, df_val), color="#f59e0b", lw=2.5, ls="--", label=f"t (df={df_val})")
    ax2.set_title("Z-distribution vs T-distribution", fontsize=13, fontweight='bold')
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close()
    st.markdown(f"""
<div class="info-box">
As df increases, the t-distribution converges to the normal distribution.
At df = {df_val}, t-critical (95%) = <strong>{t.ppf(0.975, df_val):.4f}</strong>
vs z-critical = <strong>1.9600</strong>
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CI IN PYTHON
# ═══════════════════════════════════════════════════════════════════════════════
elif "Python" in topic:
    st.title("🔬 Confidence Intervals in Python")
    st.markdown("*Live calculations using the Student Survey Dataset*")
    st.markdown("---")

    st.markdown("### Finding Z-Critical Values")
    st.markdown("""
<div class="info-box">
In Python, use <code>scipy.stats.norm.ppf()</code> - the <em>Percent Point Function</em> (inverse CDF).
</div>""", unsafe_allow_html=True)

    st.code("""from scipy.stats import norm

# 90% CI: total tail area = 0.10 → α/2 = 0.05 → area = 1 - 0.05 = 0.95
z_90 = round(norm.ppf(0.95), 3)   # → 1.645

# 95% CI: total tail area = 0.05 → α/2 = 0.025 → area = 1 - 0.025 = 0.975
z_95 = round(norm.ppf(0.975), 3)  # → 1.960

# 99% CI: total tail area = 0.01 → α/2 = 0.005 → area = 1 - 0.005 = 0.995
z_99 = round(norm.ppf(0.995), 3)  # → 2.576""", language="python")

    # Live calculation
    st.markdown("#### 🔴 Live: Calculate Any Z-Critical")
    conf_live = st.slider("Confidence Level", 0.80, 0.999, 0.95, 0.005, format="%.3f")
    alpha = 1 - conf_live
    area = 1 - alpha / 2
    z_live = norm.ppf(area)
    st.markdown(f"""
<div class="metric-card">
α = {alpha:.4f} &nbsp;|&nbsp; α/2 = {alpha/2:.4f} &nbsp;|&nbsp; Area for ppf = {area:.4f}<br>
<strong>z-critical = {z_live:.4f}</strong>
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Student Survey Dataset - Heights")
    st.markdown("""
> Dataset: 237 Statistics I students at University of Adelaide.
> We compute a **95% CI for the population mean height**.
""")

    # Simulate the dataset
    np.random.seed(42)
    n_survey = 209
    height_data = np.random.normal(172.38, 9.48, n_survey)
    height_data = np.round(height_data, 1)

    col1, col2 = st.columns([1, 1])
    with col1:
        ci_conf = st.selectbox("Choose confidence level:", [0.90, 0.95, 0.99],
                               index=1, format_func=lambda x: f"{int(x*100)}%")
        n_h = len(height_data)
        sigma_h = np.std(height_data)
        sem_h = sigma_h / np.sqrt(n_h)
        z_map = {0.90: 1.645, 0.95: 1.960, 0.99: 2.576}
        z_h = z_map[ci_conf]
        xbar_h = np.mean(height_data)
        ci_l = xbar_h - z_h * sem_h
        ci_u = xbar_h + z_h * sem_h

        st.code(f"""n     = {n_h}
sigma = np.std(height)   # {sigma_h:.4f}
sem   = sigma / np.sqrt(n)  # {sem_h:.4f}
z_crit = norm.ppf({1-(1-ci_conf)/2})  # {z_h}
xbar  = height.mean()    # {xbar_h:.4f}

ci_lower = xbar - z_crit * sem  # {ci_l:.4f}
ci_upper = xbar + z_crit * sem  # {ci_u:.4f}""", language="python")

    with col2:
        st.markdown(f"""
<div class="result-fail">
We are <strong>{int(ci_conf*100)}%</strong> confident that the true mean
student height is between<br>
<strong>{ci_l:.2f} cm</strong> and <strong>{ci_u:.2f} cm</strong>
</div>""", unsafe_allow_html=True)

        # histogram
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.hist(height_data, bins=12, color="#0d9488", edgecolor="white", alpha=0.85)
        ax.axvline(xbar_h, color="#0f1b2d", lw=2, label=f"Mean = {xbar_h:.2f}")
        ax.axvline(ci_l, color="#e11d48", lw=1.8, ls="--", label=f"Lower = {ci_l:.2f}")
        ax.axvline(ci_u, color="#f59e0b", lw=1.8, ls="--", label=f"Upper = {ci_u:.2f}")
        ax.set_xlabel("Height (cm)", fontsize=10)
        ax.set_title("Histogram of Student Height", fontsize=12, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.25)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()


# ═══════════════════════════════════════════════════════════════════════════════
# HYPOTHESIS TESTING
# ═══════════════════════════════════════════════════════════════════════════════
elif "Hypothesis" in topic:
    st.title("🧪 Hypothesis Testing")
    st.markdown("---")

    st.markdown("""
<div class="info-box">
<strong>A hypothesis</strong> is a claim about the value of a population parameter.<br>
<strong>Hypothesis testing</strong> is a decision-making process to evaluate that claim - determining whether
observed results are statistically significant or just due to chance.
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### H₀ vs H₁")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
<div class="metric-card">
<strong>Null Hypothesis (H₀)</strong><br>
The "status quo" - assumed true until disproven.<br>
Always states equality: μ = μ₀
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="metric-card">
<strong>Alternative Hypothesis (H₁)</strong><br>
What we're trying to show. Can be two-tailed, upper, or lower.
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Three Test Types")
    tabs = st.tabs(["Two-Tailed", "Upper-Tailed (Right)", "Lower-Tailed (Left)"])

    def plot_tail(test_type, alpha=0.05):
        fig, ax = plt.subplots(figsize=(8, 3.2))
        x = np.linspace(-4, 4, 500)
        y = norm.pdf(x)
        ax.plot(x, y, "#0f1b2d", lw=2)

        if test_type == "two":
            z = norm.ppf(1 - alpha/2)
            x_l = np.linspace(-4, -z, 200)
            x_r = np.linspace(z, 4, 200)
            ax.fill_between(x_l, norm.pdf(x_l), alpha=0.5, color="#e11d48", label=f"α/2 = {alpha/2}")
            ax.fill_between(x_r, norm.pdf(x_r), alpha=0.5, color="#e11d48")
            ax.axvline(-z, color="#e11d48", ls="--", lw=1.5, label=f"-z = {-z:.3f}")
            ax.axvline( z, color="#e11d48", ls="--", lw=1.5, label=f"+z = {z:.3f}")
            ax.set_title(f"Two-Tailed: Reject H₀ if |Z*| ≥ {z:.3f}", fontsize=12, fontweight='bold')

        elif test_type == "right":
            z = norm.ppf(1 - alpha)
            x_r = np.linspace(z, 4, 200)
            ax.fill_between(x_r, norm.pdf(x_r), alpha=0.5, color="#e11d48", label=f"α = {alpha}")
            ax.axvline(z, color="#e11d48", ls="--", lw=1.5, label=f"z = {z:.3f}")
            ax.set_title(f"Right-Tailed: Reject H₀ if Z* ≥ {z:.3f}", fontsize=12, fontweight='bold')

        elif test_type == "left":
            z = norm.ppf(alpha)
            x_l = np.linspace(-4, z, 200)
            ax.fill_between(x_l, norm.pdf(x_l), alpha=0.5, color="#e11d48", label=f"α = {alpha}")
            ax.axvline(z, color="#e11d48", ls="--", lw=1.5, label=f"z = {z:.3f}")
            ax.set_title(f"Left-Tailed: Reject H₀ if Z* ≤ {z:.3f}", fontsize=12, fontweight='bold')

        x_mid = np.linspace(-4, 4, 500)
        if test_type == "two":
            zz = norm.ppf(1 - alpha/2)
            x_m = np.linspace(-zz, zz, 300)
        elif test_type == "right":
            zz = norm.ppf(1 - alpha)
            x_m = np.linspace(-4, zz, 300)
        elif test_type == "left":
            zz = norm.ppf(alpha)
            x_m = np.linspace(zz, 4, 300)
        ax.fill_between(x_m, norm.pdf(x_m), alpha=0.2, color="#0d9488", label="Do not reject H₀")
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.25)
        fig.tight_layout()
        return fig

    alpha_ht = st.slider("Significance level (α)", 0.01, 0.10, 0.05, 0.01)

    with tabs[0]:
        st.markdown("**H₀: μ = μ₀   |   H₁: μ ≠ μ₀**")
        st.pyplot(plot_tail("two", alpha_ht))
        plt.close()
        st.markdown(f"""
<div class="info-box">
Reject H₀ if <strong>|Z*| ≥ {norm.ppf(1-alpha_ht/2):.4f}</strong>.
The rejection region is split equally between both tails.
</div>""", unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("**H₀: μ = μ₀   |   H₁: μ > μ₀**")
        st.pyplot(plot_tail("right", alpha_ht))
        plt.close()
        st.markdown(f"""
<div class="info-box">
Reject H₀ if <strong>Z* ≥ {norm.ppf(1-alpha_ht):.4f}</strong>.
The rejection region is in the right tail only.
</div>""", unsafe_allow_html=True)

    with tabs[2]:
        st.markdown("**H₀: μ = μ₀   |   H₁: μ < μ₀**")
        st.pyplot(plot_tail("left", alpha_ht))
        plt.close()
        st.markdown(f"""
<div class="info-box">
Reject H₀ if <strong>Z* ≤ {norm.ppf(alpha_ht):.4f}</strong>.
The rejection region is in the left tail only.
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Steps of Hypothesis Testing")
    steps = [
        ("Set up H₀ and H₁", "Define your null and alternative hypotheses clearly."),
        ("Set significance level (α)", "Typically 0.05 (5%). This controls Type I error."),
        ("Calculate test statistic (Z*)", "Z* = (x̄ − μ₀) / (σ / √n)"),
        ("Find p-value or rejection region", "Compare p-value to α, or Z* to z-critical."),
        ("Make decision", "Reject H₀ or fail to reject H₀."),
    ]
    for i, (title, desc) in enumerate(steps, 1):
        st.markdown(f"""
<div class="metric-card">
<span class="step-badge">{i}</span>
<strong>{title}</strong><br>
<span style="color:#64748b;font-size:14px;padding-left:36px">{desc}</span>
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TYPE I & II ERRORS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Type" in topic:
    st.title("⚠️ Type I & Type II Errors")
    st.markdown("---")

    st.markdown("""
<div class="info-box">
When we make a decision about H₀ based on sample data, we can be wrong in two distinct ways.
</div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
<div class="danger-box">
<strong>🔴 Type I Error (α) - False Positive</strong><br>
Rejecting H₀ when it is actually <em>true</em>.<br><br>
Concluding a result is significant when it happened purely by chance.<br><br>
<strong>Court analogy:</strong> Convicting an innocent person.
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="warning-box">
<strong>🟡 Type II Error (β) - False Negative</strong><br>
Failing to reject H₀ when it is actually <em>false</em>.<br><br>
Concluding no effect exists when one actually does.<br><br>
<strong>Court analogy:</strong> Acquitting a guilty person.
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Decision Matrix")
    col_head = st.columns([2, 2, 2])
    col_head[0].markdown("**Study Finding**")
    col_head[1].markdown("**Reality: H₀ True**")
    col_head[2].markdown("**Reality: H₀ False**")

    r1 = st.columns([2, 2, 2])
    r1[0].markdown("**Reject H₀**")
    r1[1].markdown("🔴 **Type I Error** (α)")
    r1[2].markdown("✅ **Correct** (Power = 1−β)")

    r2 = st.columns([2, 2, 2])
    r2[0].markdown("**Fail to Reject H₀**")
    r2[1].markdown("✅ **Correct**")
    r2[2].markdown("🟡 **Type II Error** (β)")

    st.markdown("---")
    st.markdown("### 🎛️ Interactive: See Type I Error in Action")
    alpha_demo = st.slider("Set significance level α", 0.01, 0.20, 0.05, 0.01)

    fig, ax = plt.subplots(figsize=(10, 4))
    x = np.linspace(-4, 4, 500)
    ax.plot(x, norm.pdf(x), "#0f1b2d", lw=2.5, label="Sampling distribution under H₀")

    z_crit = norm.ppf(1 - alpha_demo/2)
    x_l = np.linspace(-4, -z_crit, 200)
    x_r = np.linspace(z_crit, 4, 200)
    ax.fill_between(x_l, norm.pdf(x_l), alpha=0.6, color="#e11d48",
                    label=f"Type I Error (α/2 = {alpha_demo/2})")
    ax.fill_between(x_r, norm.pdf(x_r), alpha=0.6, color="#e11d48")
    x_mid = np.linspace(-z_crit, z_crit, 300)
    ax.fill_between(x_mid, norm.pdf(x_mid), alpha=0.2, color="#0d9488", label="Correct: Do not reject H₀")

    ax.axvline(-z_crit, color="#e11d48", ls="--", lw=1.5)
    ax.axvline( z_crit, color="#e11d48", ls="--", lw=1.5,
               label=f"±z-crit = ±{z_crit:.3f}")
    ax.set_title(f"Type I Error Region (α = {alpha_demo})", fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown(f"""
<div class="warning-box">
With α = {alpha_demo}, there is a <strong>{alpha_demo*100:.0f}%</strong> chance of rejecting H₀ even when it is true.
Reducing α reduces Type I error but increases Type II error.
</div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# WORKED EXAMPLE
# ═══════════════════════════════════════════════════════════════════════════════
elif "Worked" in topic:
    st.title("🔢 Worked Example - Light Bulb Lifetime")
    st.markdown("---")

    st.markdown("""
<div class="info-box">
<strong>Problem:</strong> A manufacturer claims the mean lifetime of a light bulb is
<strong>more than 10,000 hours</strong>. A sample of 30 bulbs averaged <strong>9,900 hours</strong>.
Assume population σ = 120 hours. At <strong>α = 0.05</strong>, can we reject the manufacturer's claim?
</div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎛️ Adjust Parameters")
    col1, col2, col3 = st.columns(3)
    with col1:
        xbar_ex = st.number_input("Sample Mean (x̄)", value=9900, step=10)
        mu0_ex  = st.number_input("Claimed Mean (μ₀)", value=10000, step=100)
    with col2:
        s_ex    = st.number_input("Std Deviation (σ)", value=120, min_value=1, step=5)
        n_ex    = st.number_input("Sample Size (n)", value=30, min_value=2, step=1)
    with col3:
        alpha_ex = st.selectbox("Significance (α)", [0.01, 0.05, 0.10], index=1)
        test_ex  = st.selectbox("Test Type", ["Lower-tailed (H₁: μ < μ₀)",
                                               "Upper-tailed (H₁: μ > μ₀)",
                                               "Two-tailed (H₁: μ ≠ μ₀)"])

    # Compute
    sem_ex = s_ex / np.sqrt(n_ex)
    t_stat = (xbar_ex - mu0_ex) / sem_ex
    df_ex  = n_ex - 1

    if "Lower" in test_ex:
        t_crit = -t.ppf(1 - alpha_ex, df_ex)
        p_val  = t.cdf(t_stat, df_ex)
        reject = t_stat <= t_crit
        h1_str = f"H₁: μ < {mu0_ex}"
    elif "Upper" in test_ex:
        t_crit = t.ppf(1 - alpha_ex, df_ex)
        p_val  = 1 - t.cdf(t_stat, df_ex)
        reject = t_stat >= t_crit
        h1_str = f"H₁: μ > {mu0_ex}"
    else:
        t_crit = t.ppf(1 - alpha_ex/2, df_ex)
        p_val  = 2 * (1 - t.cdf(abs(t_stat), df_ex))
        reject = abs(t_stat) >= t_crit
        h1_str = f"H₁: μ ≠ {mu0_ex}"

    st.markdown("---")
    st.markdown("### Step-by-Step Solution")

    st.markdown(f"""
<div class="metric-card">
<span class="step-badge">1</span><strong>Hypotheses</strong><br>
<span style="padding-left:36px">H₀: μ = {mu0_ex} &nbsp;&nbsp;|&nbsp;&nbsp; {h1_str}</span>
</div>
<div class="metric-card">
<span class="step-badge">2</span><strong>Test Statistic</strong><br>
<span style="padding-left:36px">t* = (x̄ − μ₀) / (s / √n) = ({xbar_ex} − {mu0_ex}) / ({s_ex} / √{n_ex}) = <strong>{t_stat:.4f}</strong></span>
</div>
<div class="metric-card">
<span class="step-badge">3</span><strong>Critical Value</strong> (df = {df_ex})<br>
<span style="padding-left:36px">t-critical = <strong>{"±" if "Two" in test_ex else ""}{abs(t_crit):.4f}</strong></span>
</div>
<div class="metric-card">
<span class="step-badge">4</span><strong>P-value</strong><br>
<span style="padding-left:36px">p-value = <strong>{p_val:.6f}</strong>  {"< α → Reject H₀" if reject else "> α → Fail to Reject H₀"}</span>
</div>""", unsafe_allow_html=True)

    if reject:
        st.markdown(f"""
<div class="result-reject">
✗ REJECT H₀<br>
<span style="font-size:14px;font-weight:400">
At α = {alpha_ex}, the test statistic ({t_stat:.4f}) falls in the rejection region.
We have sufficient evidence to reject the manufacturer's claim.
</span>
</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
<div class="result-fail">
✓ FAIL TO REJECT H₀<br>
<span style="font-size:14px;font-weight:400">
At α = {alpha_ex}, the test statistic ({t_stat:.4f}) does not fall in the rejection region.
Insufficient evidence to reject the claim.
</span>
</div>""", unsafe_allow_html=True)

    # Python code
    st.markdown("---")
    st.markdown("### Python Code")
    st.code(f"""import numpy as np
from scipy.stats import t

xbar = {xbar_ex}
mu   = {mu0_ex}
s    = {s_ex}
n    = {n_ex}
alpha = {alpha_ex}

t_stat = (xbar - mu) / (s / np.sqrt(n))
print("Test statistic:", t_stat)  # {t_stat:.6f}

# Critical value (df = n-1 = {df_ex})
t_crit = t.ppf(1 - alpha, df={df_ex})
print("t-critical:", -t_crit)     # {-abs(t_crit):.6f}

# p-value
p_value = t.cdf(t_stat, df={df_ex})
print("p-value:", p_value)        # {p_val:.8f}

# 95% Confidence Interval
z_crit = 1.96
sem    = s / np.sqrt(n)           # {sem_ex:.4f}
ci_lower = xbar - z_crit * sem   # {xbar_ex - 1.96*sem_ex:.2f}
ci_upper = xbar + z_crit * sem   # {xbar_ex + 1.96*sem_ex:.2f}
print(f"95% CI: ({'{ci_lower:.2f}'}, {'{ci_upper:.2f}'})")""", language="python")

    # Visual
    st.markdown("---")
    st.markdown("### Visualisation")
    fig, ax = plt.subplots(figsize=(10, 4))
    x_v = np.linspace(-5, 5, 500)
    ax.plot(x_v, t.pdf(x_v, df_ex), "#0f1b2d", lw=2.5, label=f"t-dist (df={df_ex})")

    if "Lower" in test_ex:
        tc = -abs(t_crit)
        x_sh = np.linspace(-5, tc, 200)
        ax.fill_between(x_sh, t.pdf(x_sh, df_ex), alpha=0.5, color="#e11d48", label="Rejection region")
        ax.axvline(tc, color="#e11d48", ls="--", lw=1.8, label=f"t-crit = {tc:.3f}")
    elif "Upper" in test_ex:
        tc = abs(t_crit)
        x_sh = np.linspace(tc, 5, 200)
        ax.fill_between(x_sh, t.pdf(x_sh, df_ex), alpha=0.5, color="#e11d48", label="Rejection region")
        ax.axvline(tc, color="#e11d48", ls="--", lw=1.8, label=f"t-crit = {tc:.3f}")
    else:
        tc = abs(t_crit)
        ax.fill_between(np.linspace(-5, -tc, 200), t.pdf(np.linspace(-5,-tc,200), df_ex),
                        alpha=0.5, color="#e11d48", label="Rejection region")
        ax.fill_between(np.linspace(tc, 5, 200), t.pdf(np.linspace(tc,5,200), df_ex),
                        alpha=0.5, color="#e11d48")
        ax.axvline(-tc, color="#e11d48", ls="--", lw=1.8)
        ax.axvline( tc, color="#e11d48", ls="--", lw=1.8, label=f"±t-crit = ±{tc:.3f}")

    colour_ts = "#e11d48" if reject else "#0d9488"
    ax.axvline(t_stat, color=colour_ts, lw=2.5, label=f"t* = {t_stat:.4f}")
    ax.set_title("Hypothesis Test - t-distribution", fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()


# ═══════════════════════════════════════════════════════════════════════════════
# QUIZ
# ═══════════════════════════════════════════════════════════════════════════════
elif "Quiz" in topic:
    st.title("🎮 Knowledge Check")
    st.markdown("*Test your understanding of the lecture*")
    st.markdown("---")

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answered" not in st.session_state:
        st.session_state.answered = {}

    questions = [
        {
            "q": "What does a 95% Confidence Interval mean?",
            "opts": [
                "95% of data values fall within the interval",
                "We are 95% confident the true population mean lies within the interval",
                "The interval contains the sample mean 95% of the time",
                "There is a 5% probability the null hypothesis is true",
            ],
            "ans": 1,
            "exp": "A 95% CI means we are 95% confident the true population parameter lies within the computed interval."
        },
        {
            "q": "A researcher uses a sample of n=25 from a normally distributed population. Which distribution should be used for the CI?",
            "opts": ["Z-distribution (standard normal)", "t-distribution", "Binomial distribution", "Chi-square distribution"],
            "ans": 1,
            "exp": "For small samples (n < 30) from a normal population, we use the t-distribution with df = n-1."
        },
        {
            "q": "What is the z-critical value for a 95% confidence interval?",
            "opts": ["1.282", "1.645", "1.960", "2.576"],
            "ans": 2,
            "exp": "For a 95% CI: α = 0.05, α/2 = 0.025, so z = norm.ppf(0.975) = 1.960."
        },
        {
            "q": "Rejecting H₀ when it is actually true is called:",
            "opts": ["Type II Error", "Type I Error", "Power Error", "Standard Error"],
            "ans": 1,
            "exp": "A Type I Error (α) is a false positive - rejecting H₀ when it is true."
        },
        {
            "q": "For a lower-tailed test with α=0.05 and t*=-4.56, t-critical=-1.699, what do we conclude?",
            "opts": [
                "Fail to reject H₀ because t* > t-critical",
                "Reject H₀ because t* < t-critical",
                "Fail to reject H₀ because the p-value > α",
                "Cannot determine without more information",
            ],
            "ans": 1,
            "exp": "For a lower-tailed test, reject H₀ if t* ≤ t-critical. Since -4.56 ≤ -1.699, we reject H₀."
        },
        {
            "q": "The Standard Error of the Mean formula is:",
            "opts": ["SE = σ × √n", "SE = σ / √n", "SE = μ / σ", "SE = σ² / n"],
            "ans": 1,
            "exp": "SE = σ/√n. As sample size increases, the standard error decreases."
        },
    ]

    score = 0
    for i, q in enumerate(questions):
        st.markdown(f"#### Q{i+1}: {q['q']}")
        key = f"q{i}"
        selected = st.radio("", q["opts"], index=None, key=key, label_visibility="collapsed")

        if selected is not None:
            correct_idx = q["ans"]
            if q["opts"].index(selected) == correct_idx:
                st.success(f"✅ Correct! {q['exp']}")
                score += 1
            else:
                st.error(f"❌ Incorrect. Correct answer: **{q['opts'][correct_idx]}**  \n{q['exp']}")
        st.markdown("---")

    if any(st.radio.__name__ for _ in []):
        pass

    answered = sum(1 for i in range(len(questions))
                   if st.session_state.get(f"q{i}") is not None)
    if answered == len(questions):
        pct = score / len(questions) * 100
        if pct >= 80:
            st.balloons()
            st.markdown(f"""
<div class="result-fail">
🎉 Excellent! You scored {score}/{len(questions)} ({pct:.0f}%)
</div>""", unsafe_allow_html=True)
        elif pct >= 50:
            st.markdown(f"""
<div class="warning-box">
Good effort! You scored {score}/{len(questions)} ({pct:.0f}%). Review the sections you missed.
</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div class="danger-box">
You scored {score}/{len(questions)} ({pct:.0f}%). Please revisit the lecture material.
</div>""", unsafe_allow_html=True)
