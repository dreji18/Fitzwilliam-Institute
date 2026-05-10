import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
from math import comb, factorial

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Data Analytics · Class 5",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

# ─── THEME ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

.hero { padding: 2rem 0 1.5rem; border-bottom: 1px solid #e0e0e0; margin-bottom: 1.5rem; }
.hero-eyebrow { font-size: .75rem; letter-spacing: .2em; color: #5c7cfa; text-transform: uppercase; margin-bottom: .4rem; }
.hero h1 { font-family: 'Syne', sans-serif; font-size: 2.6rem; font-weight: 800; letter-spacing: -1px; margin: 0 0 .4rem; line-height: 1.1; }
.hero h1 span { background: linear-gradient(120deg, #5c7cfa, #38d9a9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero p { color: #888; font-size: .85rem; margin: 0; }

.sec-title { font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 700; color: #5c7cfa; margin-bottom: .2rem; }
.sec-sub { color: #888; font-size: .8rem; margin-bottom: 1.2rem; }

.formula { background: #f0f4ff; border-left: 3px solid #5c7cfa; border-radius: 0 6px 6px 0; padding: .8rem 1.2rem; font-size: .88rem; color: #1a237e; margin: .6rem 0 1.2rem; line-height: 1.7; font-family: 'DM Mono', monospace; }

.pill-row { display: flex; flex-wrap: wrap; gap: .5rem; margin: .8rem 0 1.2rem; }
.pill { background: #f0f4ff; border: 1px solid #c5cae9; border-radius: 999px; padding: .3rem .9rem; font-size: .8rem; color: #1a237e; font-family: 'DM Mono', monospace; }
.pill b { color: #1565c0; font-weight: normal; }

.ccard { background: #f8f9ff; border: 1px solid #e3e8ff; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: .8rem; }
.ccard h4 { font-family: 'Syne', sans-serif; font-size: .95rem; font-weight: 700; color: #1a237e; margin: 0 0 .4rem; }
.ccard p { color: #555; font-size: .82rem; line-height: 1.6; margin: 0; }

.answer-box { background: #e8f5e9; border: 1px solid #43a047; border-radius: 8px; padding: .9rem 1.2rem; font-size: .88rem; color: #1b5e20; margin-top: .6rem; font-family: 'DM Mono', monospace; }

.step { display: flex; gap: .8rem; align-items: flex-start; margin-bottom: .7rem; }
.step-num { min-width: 28px; height: 28px; background: #5c7cfa; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-family: 'Syne', sans-serif; font-size: .8rem; font-weight: 700; color: #fff; flex-shrink: 0; }
.step-body { color: #222; font-size: .84rem; line-height: 1.6; padding-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ─── PLOT HELPERS ────────────────────────────────────────────────────────────
BG, SURF, GRID = "#0b0e1a", "#12172a", "#1a1f33"
AC, GR, RS, GD = "#5c7cfa", "#38d9a9", "#ff6b6b", "#ffd43b"
FONT = "DM Mono, monospace"

def base_layout(**kw):
    xa = dict(gridcolor=GRID, zerolinecolor=GRID, showline=False)
    ya = dict(gridcolor=GRID, zerolinecolor=GRID, showline=False)
    xa.update(kw.pop("xaxis", {}))
    ya.update(kw.pop("yaxis", {}))
    return dict(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(family=FONT, color="#e9ecf5", size=11),
        xaxis=xa, yaxis=ya,
        margin=dict(l=45, r=20, t=50, b=40),
        **kw,
    )

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎲 5")
    st.caption("Data Analytics · Fitzwilliam Institute · Deepak John Reji")
    st.markdown("---")
    topic = st.radio("", [
        "🏠 Overview",
        "🎲 Probability Basics",
        "🔀 Compound Events",
        "✏️ Exercises",
        "📦 Random Variables",
        "🔵 Bernoulli & Binomial",
        "〰️ Continuous & Normal",
        "📐 Z-Scores",
        "🔔 Sampling & CLT",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.caption("Lecture 4 · April 16, 2026")

# ════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if topic == "🏠 Overview":
    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">Diploma in Data Analytics · Lecture 4</div>
        <h1>Probability &<br><span>Probability Distributions</span></h1>
        <p>Fitzwilliam Institute · April 16, 2026 · Deepak John Reji</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    for col, icon, title, body in [
        (c1, "🎲", "Probability Basics", "Sample spaces, events, and the rules of probability. Coins, dice, and relative frequencies."),
        (c2, "🔀", "Compound Events", "Union, intersection, independence. Addition rule for disjoint and non-disjoint events."),
        (c3, "✏️", "Exercises", "Fruit basket, card draws - step-by-step worked solutions with interactive verification."),
    ]:
        col.markdown(f'<div class="ccard"><h4>{icon} {title}</h4><p>{body}</p></div>', unsafe_allow_html=True)

    c4, c5, c6 = st.columns(3)
    for col, icon, title, body in [
        (c4, "📦", "Random Variables", "Discrete vs continuous, PMF, CDF - and why not all values are equally likely."),
        (c5, "🔵", "Bernoulli & Binomial", "From a single trial to n trials. The jury example and the faulty-component problem."),
        (c6, "〰️ / 📐", "Normal & Z-Scores", "Bell curve, μ and σ, standardisation, the empirical rule - calculator battery example."),
    ]:
        col.markdown(f'<div class="ccard"><h4>{icon} {title}</h4><p>{body}</p></div>', unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.info("👈 Pick a topic from the sidebar. Every section is interactive - adjust sliders and check your answers on the exercises.")

# ════════════════════════════════════════════════════════════════════════════
# PROBABILITY BASICS
# ════════════════════════════════════════════════════════════════════════════
elif topic == "🎲 Probability Basics":
    st.markdown('<div class="sec-title">Probability Basics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Quantitative measure of uncertainty · Sample space · Events</div>', unsafe_allow_html=True)

    tab_c, tab_sim = st.tabs(["Concepts", "Relative Frequency Simulator"])

    with tab_c:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**What is probability?**")
            st.markdown("A number between 0 and 1 measuring how likely an event will occur when an experiment is performed.")
            st.markdown('<div class="formula">0 = impossible · 1 = certain<br>P(Ω) = 1  (entire sample space)<br>P(A) = |A| / |Ω|  (equally likely outcomes)</div>', unsafe_allow_html=True)
            st.markdown("**Steps to calculate P(A)**")
            for num, text in [
                ("1", "Get the sample space Ω"),
                ("2", "Assign probabilities to each sample point"),
                ("3", "Identify sample points in event A"),
                ("4", "Sum their probabilities"),
            ]:
                st.markdown(f'<div class="step"><div class="step-num">{num}</div><div class="step-body">{text}</div></div>', unsafe_allow_html=True)

        with col2:
            st.markdown("**Example: roll a fair die - P(even number)?**")
            st.markdown('<div class="formula">Ω = {1, 2, 3, 4, 5, 6} each with prob 1/6<br>A = {2, 4, 6}<br>P(A) = 1/6 + 1/6 + 1/6 = 1/2</div>', unsafe_allow_html=True)
            st.markdown("**Die probability explorer**")
            outcomes = st.multiselect("Select outcomes of interest", [1,2,3,4,5,6], default=[2,4,6])
            prob = len(outcomes)/6 if outcomes else 0
            st.markdown(f'<div class="pill-row"><div class="pill">Selected: <b>{outcomes}</b></div><div class="pill">P(A) = <b>{len(outcomes)}/6 = {prob:.4f}</b></div></div>', unsafe_allow_html=True)

    with tab_sim:
        st.markdown("**Coke-can toss** - Watch how relative frequency converges to the true probability (the lecture example: 10/100 tosses upright → P ≈ 0.1)")
        c1, c2 = st.columns([1,2])
        true_p  = c1.slider("True probability p", 0.01, 0.99, 0.10, 0.01)
        n_toss  = c1.slider("Number of tosses", 10, 5000, 500, 10)
        n_paths = c1.slider("Paths", 1, 5, 3)

        np.random.seed(None)
        fig = go.Figure()
        colors = [AC, GR, RS, GD, "#c77dff"]
        for i in range(n_paths):
            draws = np.random.binomial(1, true_p, n_toss)
            cum_freq = np.cumsum(draws) / np.arange(1, n_toss+1)
            fig.add_scatter(x=np.arange(1, n_toss+1), y=cum_freq,
                            mode="lines", line=dict(color=colors[i], width=1.8),
                            name=f"Path {i+1}", opacity=0.9)
        fig.add_hline(y=true_p, line_color="white", line_dash="dot", line_width=2,
                      annotation_text=f"True p = {true_p}", annotation_font_color="white")
        fig.update_layout(**base_layout(title="Relative Frequency converging to True Probability",
                          xaxis_title="Number of tosses", yaxis_title="Relative frequency",
                          height=380, xaxis=dict(type="log"), legend=dict(bgcolor="rgba(0,0,0,0)")))
        c2.plotly_chart(fig, use_container_width=True)
        c2.caption("x-axis is log-scaled. Even for small p, frequency converges.")

# ════════════════════════════════════════════════════════════════════════════
# COMPOUND EVENTS
# ════════════════════════════════════════════════════════════════════════════
elif topic == "🔀 Compound Events":
    st.markdown('<div class="sec-title">Compound Events</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Independence · Intersection (A∩B) · Union (A∪B) · Addition Rule</div>', unsafe_allow_html=True)

    tab_c, tab_die, tab_venn = st.tabs(["Rules", "Die Example (Slide 10)", "Venn Simulator"])

    with tab_c:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Independence**")
            st.markdown("Two events are independent if one occurring does not change the probability of the other.")
            st.markdown('<div class="formula">P(A ∩ B) = P(A) × P(B)  [independent only]</div>', unsafe_allow_html=True)
            st.markdown("*Example: rolling a 2 on a die AND flipping heads on a coin.*")
        with col2:
            st.markdown("**Addition Rule**")
            st.markdown('<div class="formula">Disjoint (mutually exclusive):<br>P(A∪B) = P(A) + P(B)<br><br>Non-disjoint:<br>P(A∪B) = P(A) + P(B) - P(A∩B)</div>', unsafe_allow_html=True)

    with tab_die:
        st.markdown("**Slide 10 Example - Toss a fair die.**")
        st.markdown("Event **A**: Even number {2, 4, 6}  ·  Event **B**: ≤ 3 → {1, 2, 3}")

        A = {2, 4, 6}
        B = {1, 2, 3}
        AiB = A & B
        AuB = A | B
        pA, pB = len(A)/6, len(B)/6
        pAiB, pAuB = len(AiB)/6, len(AuB)/6

        col1, col2 = st.columns(2)
        col1.markdown(f'<div class="formula">A = {sorted(A)}<br>B = {sorted(B)}<br>A ∩ B = {sorted(AiB)}  P(A∩B) = {len(AiB)}/6 = {pAiB:.4f}<br>A ∪ B = {sorted(AuB)}  P(A∪B) = {len(AuB)}/6 = {pAuB:.4f}</div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="formula">P(A∪B) via Addition Rule:<br>P(A) + P(B) - P(A∩B)<br>= {pA:.4f} + {pB:.4f} - {pAiB:.4f}<br>= {pAuB:.4f}</div>', unsafe_allow_html=True)

        die_faces = list(range(1, 7))
        bar_colors = []
        for f in die_faces:
            if f in AiB:   bar_colors.append(GD)
            elif f in A:   bar_colors.append(AC)
            elif f in B:   bar_colors.append(GR)
            else:          bar_colors.append(SURF)
        fig = go.Figure(go.Bar(x=[str(f) for f in die_faces], y=[1/6]*6,
                               marker_color=bar_colors, text=["1/6"]*6, textposition="inside"))
        fig.update_layout(**base_layout(title="Die faces coloured by event membership",
                          xaxis_title="Face", yaxis_title="Probability", height=270,
                          yaxis=dict(range=[0, 0.25])))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<div class="pill-row"><div class="pill" style="border-color:{AC}">A only (blue)</div><div class="pill" style="border-color:{GR}">B only (green)</div><div class="pill" style="border-color:{GD}">A∩B (gold) = {{2}}</div><div class="pill">Neither = {{5}}</div></div>', unsafe_allow_html=True)

    with tab_venn:
        st.markdown("**Interactive Venn - adjust P(A), P(B) and their overlap**")
        c1, c2, c3 = st.columns(3)
        pA  = c1.slider("P(A)", 0.05, 0.9, 0.5, 0.05)
        pB  = c2.slider("P(B)", 0.05, 0.9, 0.4, 0.05)
        pAB = c3.slider("P(A∩B)", 0.0, float(min(pA, pB)), min(0.2, float(min(pA, pB))), 0.05)
        pAuB = min(pA + pB - pAB, 1.0)

        st.markdown(f'<div class="pill-row"><div class="pill">P(A) = <b>{pA:.2f}</b></div><div class="pill">P(B) = <b>{pB:.2f}</b></div><div class="pill">P(A∩B) = <b>{pAB:.2f}</b></div><div class="pill">P(A∪B) = <b>{pAuB:.2f}</b></div><div class="pill">P(Aᶜ) = <b>{1-pA:.2f}</b></div></div>', unsafe_allow_html=True)

        cx_a, cx_b = -0.45, 0.45
        fig = go.Figure()
        fig.add_shape(type="circle", x0=cx_a-1, y0=-1, x1=cx_a+1, y1=1,
                      fillcolor=f"rgba(92,124,250,{pA*0.5})", line_color=AC, line_width=2.5)
        fig.add_shape(type="circle", x0=cx_b-1, y0=-1, x1=cx_b+1, y1=1,
                      fillcolor=f"rgba(255,107,107,{pB*0.5})", line_color=RS, line_width=2.5)
        fig.add_annotation(x=cx_a-0.55, y=0, text=f"A only<br>{pA-pAB:.2f}", showarrow=False,
                            font=dict(color=AC, size=14, family=FONT))
        fig.add_annotation(x=0, y=0, text=f"A∩B<br>{pAB:.2f}", showarrow=False,
                            font=dict(color=GD, size=14, family=FONT))
        fig.add_annotation(x=cx_b+0.55, y=0, text=f"B only<br>{pB-pAB:.2f}", showarrow=False,
                            font=dict(color=RS, size=14, family=FONT))
        fig.update_layout(**base_layout(height=290,
                          xaxis=dict(visible=False), yaxis=dict(visible=False, scaleanchor="x")))
        st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# EXERCISES
# ════════════════════════════════════════════════════════════════════════════
elif topic == "✏️ Exercises":
    st.markdown('<div class="sec-title">Exercises from Slide 11</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Work through each problem, then reveal the solution</div>', unsafe_allow_html=True)

    st.markdown("### Exercise 1 · Fruit Basket")
    st.markdown("A large basket contains **3 oranges, 2 apples and 5 bananas**. If a piece of fruit is chosen at random, what is the probability of getting an **orange or a banana**?")

    with st.expander("💡 Show Solution"):
        total = 10
        p_orange = 3/total
        p_banana = 5/total
        p_either = p_orange + p_banana
        st.markdown(f"""
        <div class="answer-box">
        Oranges and bananas are disjoint - a fruit cannot be both.<br><br>
        Total fruit = 3 + 2 + 5 = <b>{total}</b><br>
        P(orange) = 3/{total} = {p_orange:.4f}<br>
        P(banana) = 5/{total} = {p_banana:.4f}<br><br>
        P(orange ∪ banana) = P(orange) + P(banana)  [disjoint - no overlap]<br>
        = {p_orange:.4f} + {p_banana:.4f} = <b>{p_either:.4f} = 4/5</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("**Try it:** Change basket counts and recompute")
    c1, c2, c3 = st.columns(3)
    n_o = c1.number_input("Oranges", 1, 20, 3)
    n_a = c2.number_input("Apples",  1, 20, 2)
    n_b = c3.number_input("Bananas", 1, 20, 5)
    tot = n_o + n_a + n_b
    st.markdown(f'<div class="pill-row"><div class="pill">P(orange) = <b>{n_o/tot:.4f}</b></div><div class="pill">P(banana) = <b>{n_b/tot:.4f}</b></div><div class="pill">P(orange or banana) = <b>{(n_o+n_b)/tot:.4f}</b></div></div>', unsafe_allow_html=True)

    st.divider()

    st.markdown("### Exercise 2 · Card Draws with Replacement")
    st.markdown("Three cards are chosen **with replacement** from a standard deck. What is the probability that **all three are lower than 6**? *(Ace & Joker rank higher than King; standard 52-card deck)*")

    with st.expander("💡 Show Solution"):
        favourable = 16
        p_one = favourable / 52
        p_three = p_one ** 3
        st.markdown(f"""
        <div class="answer-box">
        Cards lower than 6 (i.e. 2, 3, 4, 5) = 4 values × 4 suits = <b>{favourable} cards</b><br>
        P(one card &lt; 6) = {favourable}/52 = {p_one:.6f}<br><br>
        Draws are <b>independent</b> (with replacement), so:<br>
        P(all three &lt; 6) = P(card &lt; 6)³ = ({favourable}/52)³<br>
        = {p_one:.6f}³ = <b>{p_three:.6f}</b>
        </div>
        """, unsafe_allow_html=True)

    n_draws = st.slider("Number of draws (with replacement)", 1, 6, 3)
    p_low  = 16/52
    p_all  = p_low ** n_draws
    st.markdown(f'<div class="pill-row"><div class="pill">P(one card &lt;6) = <b>{p_low:.4f}</b></div><div class="pill">P(all {n_draws} cards &lt;6) = <b>{p_all:.6f}</b></div></div>', unsafe_allow_html=True)

    st.divider()

    st.markdown("### Exercise 3 · Ace from a Deck")
    st.markdown("What is the probability that a single card chosen from a deck is an **ace**?")

    with st.expander("💡 Show Solution"):
        st.markdown(f"""
        <div class="answer-box">
        There are 4 aces in a standard 52-card deck (one per suit).<br><br>
        P(ace) = 4/52 = <b>1/13 ≈ 0.0769</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<div class="pill-row"><div class="pill">P(ace) = 4/52 = <b>{4/52:.4f}</b></div><div class="pill">1 in <b>13</b> chance</div></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# RANDOM VARIABLES
# ════════════════════════════════════════════════════════════════════════════
elif topic == "📦 Random Variables":
    st.markdown('<div class="sec-title">Random Variables & Distributions</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">PMF · CDF · Discrete vs Continuous</div>', unsafe_allow_html=True)

    tab_c, tab_pmf, tab_cdf = st.tabs(["Concepts", "PMF Explorer", "CDF Explorer"])

    with tab_c:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="ccard"><h4>Random Variable</h4><p>A random number drawn from a population. Its value is unknown before observation and determined by chance. Once observed it is fixed.</p></div>
            <div class="ccard"><h4>Discrete RV</h4><p>Takes only whole number (integer) values. E.g. number of jurors voting guilty, number of faults in a batch. Described by a <b>probability mass function (PMF)</b>.</p></div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="formula">p(x) = P(X = x)<br>pmf is non-negative<br>Σ p(x) = 1</div>', unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="ccard"><h4>Continuous RV</h4><p>Can take any real value in some range. Usually from measurements: height, time, price. Probabilities are written as P(a &lt; X ≤ b) - area under the pdf.</p></div>
            <div class="ccard"><h4>CDF</h4><p>F(x) = P(X ≤ x). Gives the probability that the variable is at most x. Works for both discrete and continuous RVs.</p></div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="formula">F(x) = P(X ≤ x)<br>Non-decreasing, F(-∞)=0, F(+∞)=1</div>', unsafe_allow_html=True)

    with tab_pmf:
        st.markdown("**Build a simple discrete PMF** - assign probabilities to outcomes of a 4-sided die")
        cols = st.columns(4)
        raw = [cols[i].number_input(f"P(X={i+1})", 0.0, 1.0, 0.25, 0.05, key=f"pmf{i}") for i in range(4)]
        total_p = sum(raw)
        valid = abs(total_p - 1.0) < 0.01
        fig = go.Figure(go.Bar(x=[1,2,3,4], y=raw, marker_color=[AC,GR,RS,GD]))
        fig.update_layout(**base_layout(
            title=f"PMF - sum = {total_p:.3f} {'✓ valid' if valid else '✗ must sum to 1'}",
            xaxis_title="x", yaxis_title="p(x)", height=300))
        st.plotly_chart(fig, use_container_width=True)
        if not valid:
            st.warning(f"Probabilities sum to {total_p:.3f}. A valid PMF must sum to exactly 1.")

    with tab_cdf:
        st.markdown("**CDF of the same distribution**")
        cum = np.cumsum(raw)
        fig = go.Figure()
        for i, (x_val, y_val) in enumerate(zip([1,2,3,4], cum)):
            x_end = x_val + 1 if x_val < 4 else 4.5
            fig.add_shape(type="line", x0=x_val, x1=x_end, y0=y_val, y1=y_val,
                          line=dict(color=AC, width=3))
            fig.add_scatter(x=[x_val], y=[y_val], mode="markers",
                            marker=dict(color=AC, size=9, symbol="circle"), showlegend=False)
        fig.update_layout(**base_layout(title="CDF - F(x) = P(X ≤ x)",
                          xaxis_title="x", yaxis_title="F(x)", height=300,
                          xaxis=dict(range=[0.5, 5]), yaxis=dict(range=[-0.05, 1.1])))
        st.plotly_chart(fig, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# BERNOULLI & BINOMIAL
# ════════════════════════════════════════════════════════════════════════════
elif topic == "🔵 Bernoulli & Binomial":
    st.markdown('<div class="sec-title">Bernoulli & Binomial Distributions</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">From a single trial to n independent trials</div>', unsafe_allow_html=True)

    tab_bern, tab_binom, tab_jury, tab_fault = st.tabs(["Bernoulli", "Binomial", "Jury Example", "Faulty Components"])

    with tab_bern:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Bernoulli Distribution**")
            st.markdown("Models a single trial with exactly two outcomes: success (1) or failure (0).")
            st.markdown('<div class="formula">P(X=1) = p  (success)<br>P(X=0) = 1-p  (failure)<br><br>E[X] = p<br>Var(X) = p(1-p)</div>', unsafe_allow_html=True)
            st.markdown("**Applications:** Win/Loss · Pass/Fail · Clicked ad / Did not click")
        with col2:
            p_b = st.slider("p (probability of success)", 0.01, 0.99, 0.5, 0.01)
            fig = go.Figure(go.Bar(x=["Failure (0)", "Success (1)"], y=[1-p_b, p_b],
                                   marker_color=[RS, GR], text=[f"{1-p_b:.3f}", f"{p_b:.3f}"],
                                   textposition="outside"))
            fig.update_layout(**base_layout(title=f"Bernoulli(p={p_b:.2f})",
                              yaxis_title="Probability", height=300, yaxis=dict(range=[0, 1.1])))
            st.plotly_chart(fig, use_container_width=True)

    with tab_binom:
        st.markdown("**Binomial** = sum of n independent Bernoulli(p) trials")
        st.markdown('<div class="formula">X ~ Binomial(n, p)<br>P(X=k) = C(n,k) · p^k · (1-p)^(n-k)<br>E[X] = np  ·  Var(X) = np(1-p)</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        n_b = c1.slider("n (trials)", 1, 50, 12)
        p_b2 = c2.slider("p (success prob)", 0.01, 0.99, 0.5, 0.01, key="binom_p")
        x = np.arange(0, n_b+1)
        pmf = stats.binom.pmf(x, n_b, p_b2)
        cdf_b = stats.binom.cdf(x, n_b, p_b2)

        fig = make_subplots(rows=1, cols=2, subplot_titles=["PMF - P(X=k)", "CDF - P(X<=k)"])
        fig.add_bar(x=x, y=pmf, marker_color=AC, row=1, col=1)
        fig.add_scatter(x=x, y=cdf_b, mode="lines+markers",
                        line=dict(color=GR, width=2), marker=dict(size=5), row=1, col=2)
        fig.update_layout(**base_layout(title=f"Binomial(n={n_b}, p={p_b2:.2f})", height=340))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<div class="pill-row"><div class="pill">E[X] = np = <b>{n_b*p_b2:.3f}</b></div><div class="pill">Var(X) = <b>{n_b*p_b2*(1-p_b2):.3f}</b></div><div class="pill">SD = <b>{np.sqrt(n_b*p_b2*(1-p_b2)):.3f}</b></div></div>', unsafe_allow_html=True)

    with tab_jury:
        st.markdown("**Slide 20 - Jury Example**")
        st.markdown("12 jurors, each independently votes Guilty with probability p. X = number of guilty votes → X ~ Binomial(12, p)")
        p_jury = st.slider("P(Guilty vote)", 0.01, 0.99, 0.5, 0.01, key="jury_p")
        x_j = np.arange(0, 13)
        pmf_j = stats.binom.pmf(x_j, 12, p_jury)
        fig = go.Figure(go.Bar(x=x_j, y=pmf_j, marker_color=AC,
                               text=[f"{v:.3f}" for v in pmf_j], textposition="outside",
                               textfont=dict(size=9)))
        fig.update_layout(**base_layout(title=f"Jury: Binomial(12, {p_jury:.2f})",
                          xaxis_title="# guilty votes", yaxis_title="Probability", height=340))
        st.plotly_chart(fig, use_container_width=True)

        k_q = st.slider("Query: P(X = k)", 0, 12, 6)
        st.markdown(f'<div class="pill-row"><div class="pill">P(X={k_q}) = <b>{stats.binom.pmf(k_q,12,p_jury):.6f}</b></div><div class="pill">P(X≤{k_q}) = <b>{stats.binom.cdf(k_q,12,p_jury):.6f}</b></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="formula">Python equivalent:<br>from scipy.stats import binom<br>binom.pmf({k_q}, 12, {p_jury:.2f})  # PMF<br>binom.cdf({k_q}, 12, {p_jury:.2f})  # CDF</div>', unsafe_allow_html=True)

    with tab_fault:
        st.markdown("**Slide 22 - Faulty Components**")
        st.markdown("An engineer tests **6 items**. Each is independently faulty with probability p=0.1.")

        p_f = st.slider("P(faulty)", 0.01, 0.5, 0.1, 0.01, key="fault_p")
        n_f = st.slider("Batch size tested", 1, 20, 6, key="fault_n")
        x_f = np.arange(0, n_f+1)
        pmf_f = stats.binom.pmf(x_f, n_f, p_f)

        p_none     = stats.binom.pmf(0, n_f, p_f)
        p_one      = stats.binom.pmf(1, n_f, p_f)
        p_two_plus = 1 - stats.binom.cdf(1, n_f, p_f)

        bar_c = [GR if i==0 else AC if i==1 else RS for i in x_f]
        fig = go.Figure(go.Bar(x=x_f, y=pmf_f, marker_color=bar_c))
        fig.update_layout(**base_layout(title=f"Binomial({n_f}, {p_f:.2f}) - Faulty Components",
                          xaxis_title="# faulty", yaxis_title="Probability", height=300))
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        col1.markdown(f'<div class="ccard" style="border-color:{GR}"><h4 style="color:{GR}">P(none faulty)</h4><p style="color:{GR};font-size:1.3rem;font-weight:700">{p_none:.6f}</p><p>All {n_f} items pass</p></div>', unsafe_allow_html=True)
        col2.markdown(f'<div class="ccard" style="border-color:{AC}"><h4 style="color:{AC}">P(exactly 1 faulty)</h4><p style="color:{AC};font-size:1.3rem;font-weight:700">{p_one:.6f}</p><p>Exactly one fails</p></div>', unsafe_allow_html=True)
        col3.markdown(f'<div class="ccard" style="border-color:{RS}"><h4 style="color:{RS}">P(2 or more faulty)</h4><p style="color:{RS};font-size:1.3rem;font-weight:700">{p_two_plus:.6f}</p><p>1 - P(0) - P(1)</p></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# CONTINUOUS & NORMAL
# ════════════════════════════════════════════════════════════════════════════
elif topic == "〰️ Continuous & Normal":
    st.markdown('<div class="sec-title">Continuous Random Variables & Normal Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">PDF · Bell curve · mu and sigma · Empirical rule</div>', unsafe_allow_html=True)

    tab_c, tab_norm, tab_emp = st.tabs(["Continuous RVs", "Normal Distribution", "Empirical Rule"])

    with tab_c:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Continuous RV examples from the lecture:**")
            for ex in ["Height of an individual",
                       "Time before the first goal in a match",
                       "Volume of product from a production process",
                       "Price of a health insurance policy"]:
                st.markdown(f"- {ex}")
            st.markdown('<div class="formula">P(X = k) = 0 for any single point<br>Instead: P(a &lt; X ≤ b) = area under pdf between a and b</div>', unsafe_allow_html=True)
        with col2:
            st.markdown("**PDF properties**")
            st.markdown("- Non-negative: f(x) >= 0 for all x")
            st.markdown("- Total area = 1: integral of f(x) dx = 1")
            st.markdown("- P(a < X <= b) = integral from a to b of f(x) dx")
            st.markdown('<div class="formula">CDF: F(x) = P(X <= x)</div>', unsafe_allow_html=True)

    with tab_norm:
        st.markdown("**Normal Distribution** X ~ N(mu, sigma^2)")
        st.markdown('<div class="formula">f(x) = (1/sigma*sqrt(2*pi)) * exp(-(x-mu)^2 / 2*sigma^2)</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        mu    = c1.slider("mu (mean)", -5.0, 5.0, 0.0, 0.5)
        sigma = c2.slider("sigma (std dev)", 0.3, 5.0, 1.0, 0.1)

        x = np.linspace(mu - 4.5*sigma, mu + 4.5*sigma, 600)
        pdf = stats.norm.pdf(x, mu, sigma)
        cdf_n = stats.norm.cdf(x, mu, sigma)

        fig = make_subplots(rows=1, cols=2, subplot_titles=["PDF - bell curve", "CDF"])
        fig.add_scatter(x=x, y=pdf, fill="tozeroy",
                        fillcolor="rgba(92,124,250,0.15)",
                        line=dict(color=AC, width=2.5), row=1, col=1)
        m1 = (x >= mu-sigma) & (x <= mu+sigma)
        fig.add_scatter(x=x[m1], y=pdf[m1], fill="tozeroy",
                        fillcolor="rgba(56,217,169,0.3)", line=dict(width=0),
                        name="±1sigma (68.3%)", row=1, col=1)
        fig.add_vline(x=mu, line_color=GD, line_dash="dot", line_width=1.5, row=1, col=1)
        fig.add_scatter(x=x, y=cdf_n, line=dict(color=GR, width=2.5), row=1, col=2)
        fig.update_layout(**base_layout(title=f"N(mu={mu}, sigma^2={sigma**2:.2f})", height=360,
                          legend=dict(bgcolor="rgba(0,0,0,0)")))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("**Compute P(a < X <= b)**")
        c1, c2 = st.columns(2)
        a_val = c1.slider("a", float(mu-4*sigma), float(mu+4*sigma), float(mu-sigma), float(sigma/10))
        b_val = c2.slider("b", float(mu-4*sigma), float(mu+4*sigma), float(mu+sigma), float(sigma/10))
        if a_val < b_val:
            prob = stats.norm.cdf(b_val, mu, sigma) - stats.norm.cdf(a_val, mu, sigma)
            st.markdown(f'<div class="pill-row"><div class="pill">P({a_val:.2f} &lt; X &lt;= {b_val:.2f}) = <b>{prob:.6f}</b></div></div>', unsafe_allow_html=True)

    with tab_emp:
        st.markdown("**Empirical Rule - the 68-95-99.7 rule**")
        mu_e    = st.slider("mu", -5.0, 5.0, 0.0, 0.5, key="emp_mu")
        sigma_e = st.slider("sigma", 0.3, 3.0, 1.0, 0.1, key="emp_sig")
        x = np.linspace(mu_e - 4*sigma_e, mu_e + 4*sigma_e, 600)
        pdf = stats.norm.pdf(x, mu_e, sigma_e)

        fig = go.Figure()
        for k, col_fill, label in [(3,"rgba(255,107,107,0.25)","±3sigma 99.7%"),
                                    (2,"rgba(92,124,250,0.25)","±2sigma 95.4%"),
                                    (1,"rgba(56,217,169,0.30)","±1sigma 68.3%")]:
            m = (x >= mu_e - k*sigma_e) & (x <= mu_e + k*sigma_e)
            fig.add_scatter(x=x[m], y=pdf[m], fill="tozeroy", fillcolor=col_fill,
                            line=dict(width=0), name=label)
        fig.add_scatter(x=x, y=pdf, line=dict(color="white", width=2), showlegend=False)
        for k in [1, 2, 3]:
            for sign in [-1, 1]:
                fig.add_vline(x=mu_e + sign*k*sigma_e, line_color=GRID, line_width=1,
                              annotation_text=f"{'+'if sign>0 else '-'}{k}s",
                              annotation_font=dict(size=10, color="#6c757d"))
        fig.update_layout(**base_layout(title="Empirical Rule",
                          xaxis_title="x", yaxis_title="f(x)", height=370,
                          legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.1)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<div class="pill-row"><div class="pill">±1sigma: <b>68.3%</b></div><div class="pill">±2sigma: <b>95.4%</b></div><div class="pill">±3sigma: <b>99.7%</b></div></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# Z-SCORES
# ════════════════════════════════════════════════════════════════════════════
elif topic == "📐 Z-Scores":
    st.markdown('<div class="sec-title">Standardisation & Z-Scores</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Convert any normal to N(0,1) · Slide 32-35 examples</div>', unsafe_allow_html=True)

    st.markdown('<div class="formula">z-score = (X - mu) / sigma<br><br>Measures distance from the mean in units of standard deviations.<br>Standardised variable Z ~ N(0,1)</div>', unsafe_allow_html=True)

    tab_calc, tab_battery = st.tabs(["Z-Score Calculator", "Battery Example (Slide 33)"])

    with tab_calc:
        c1, c2, c3 = st.columns(3)
        mu_z    = c1.number_input("mu (population mean)", value=100.0)
        sigma_z = c2.number_input("sigma (std dev)", value=15.0, min_value=0.01)
        x_z     = c3.number_input("Observed value X", value=120.0)
        z = (x_z - mu_z) / sigma_z
        p_below = stats.norm.cdf(z)
        p_above = 1 - p_below

        st.markdown(f'<div class="pill-row"><div class="pill">z = ({x_z} - {mu_z}) / {sigma_z} = <b>{z:.4f}</b></div><div class="pill">P(X &lt;= {x_z}) = <b>{p_below:.4f}</b></div><div class="pill">P(X &gt; {x_z}) = <b>{p_above:.4f}</b></div></div>', unsafe_allow_html=True)

        x_range = np.linspace(mu_z - 4*sigma_z, mu_z + 4*sigma_z, 500)
        pdf_v   = stats.norm.pdf(x_range, mu_z, sigma_z)
        fig = go.Figure()
        fig.add_scatter(x=x_range, y=pdf_v, fill="tozeroy",
                        fillcolor="rgba(92,124,250,0.1)", line=dict(color=AC, width=2))
        mask = x_range <= x_z
        fig.add_scatter(x=x_range[mask], y=pdf_v[mask], fill="tozeroy",
                        fillcolor="rgba(56,217,169,0.35)", line=dict(width=0),
                        name=f"P(X<={x_z:.1f})")
        fig.add_vline(x=x_z, line_color=GD, line_width=2,
                      annotation_text=f"X={x_z} (z={z:.2f})", annotation_font_color=GD)
        fig.add_vline(x=mu_z, line_color="rgba(255,255,255,0.33)", line_dash="dot", line_width=1.5,
                      annotation_text=f"mu={mu_z}")
        fig.update_layout(**base_layout(title=f"N({mu_z}, {sigma_z}^2) - shaded = P(X <= {x_z})",
                          xaxis_title="x", yaxis_title="f(x)", height=340,
                          legend=dict(bgcolor="rgba(0,0,0,0)")))
        st.plotly_chart(fig, use_container_width=True)

    with tab_battery:
        st.markdown("**Slide 33 - Calculator Battery Example**")
        st.markdown("X = time between charges (hours) ~ N(mu=100, sigma=15). Find P(80 < X < 120).")

        mu_bat, sigma_bat = 100, 15
        a_bat, b_bat = 80, 120
        z_a = (a_bat - mu_bat) / sigma_bat
        z_b = (b_bat - mu_bat) / sigma_bat
        prob = stats.norm.cdf(z_b) - stats.norm.cdf(z_a)

        col1, col2 = st.columns(2)
        col1.markdown(f"""
        <div class="formula">
        mu = {mu_bat}, sigma = {sigma_bat}<br><br>
        z(80)  = (80 - 100) / 15 = <b>{z_a:.4f}</b><br>
        z(120) = (120 - 100) / 15 = <b>{z_b:.4f}</b><br><br>
        P(80 &lt; X &lt; 120) = P({z_a:.2f} &lt; Z &lt; {z_b:.2f})<br>
        = Phi({z_b:.2f}) - Phi({z_a:.2f})<br>
        = <b>{prob:.6f} = {prob*100:.2f}%</b>
        </div>
        """, unsafe_allow_html=True)

        x_b = np.linspace(mu_bat - 4.5*sigma_bat, mu_bat + 4.5*sigma_bat, 600)
        pdf_b = stats.norm.pdf(x_b, mu_bat, sigma_bat)
        fig = go.Figure()
        fig.add_scatter(x=x_b, y=pdf_b, line=dict(color=AC, width=2.5))
        mask_b = (x_b >= a_bat) & (x_b <= b_bat)
        fig.add_scatter(x=x_b[mask_b], y=pdf_b[mask_b], fill="tozeroy",
                        fillcolor="rgba(56,217,169,0.4)", line=dict(width=0),
                        name=f"P(80<X<120) = {prob:.4f}")
        for v, lbl, clr in [(a_bat,"80h",GD),(b_bat,"120h",GD),(mu_bat,"mu=100h","#aaaaaa")]:
            fig.add_vline(x=v, line_color=clr, line_dash="dot", line_width=1.5,
                          annotation_text=lbl, annotation_font_color=clr)
        fig.update_layout(**base_layout(title="Battery: N(100, 15^2)",
                          xaxis_title="Hours", yaxis_title="f(x)", height=340,
                          legend=dict(bgcolor="rgba(0,0,0,0)")))
        col2.plotly_chart(fig, use_container_width=True)

        st.markdown("**Explore different intervals**")
        c1, c2 = st.columns(2)
        a2 = c1.slider("Lower bound (a)", 40, 100, 80)
        b2 = c2.slider("Upper bound (b)", 100, 160, 120)
        if a2 < b2:
            z_a2 = (a2 - mu_bat)/sigma_bat
            z_b2 = (b2 - mu_bat)/sigma_bat
            prob2 = stats.norm.cdf(z_b2) - stats.norm.cdf(z_a2)
            st.markdown(f'<div class="pill-row"><div class="pill">P({a2} &lt; X &lt; {b2}) = <b>{prob2:.6f}</b></div><div class="pill">z-scores: <b>{z_a2:.3f}</b> to <b>{z_b2:.3f}</b></div></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# SAMPLING & CLT
# ════════════════════════════════════════════════════════════════════════════
elif topic == "🔔 Sampling & CLT":
    st.markdown('<div class="sec-title">Sampling Distributions & Central Limit Theorem</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-sub">Slides 37-41 · t, F and chi-square distributions</div>', unsafe_allow_html=True)

    tab_samp, tab_clt, tab_other = st.tabs(["Sampling Distribution of X-bar", "CLT Simulator", "t / F / chi-sq"])

    with tab_samp:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Key idea from Slide 38**")
            st.markdown("The sample is one of many that could be drawn. The statistic (e.g. X-bar) varies across samples - it is itself a random variable with its own distribution.")
            st.markdown('<div class="formula">E[X-bar] = mu  (same as population mean)<br><br>SE(X-bar) = sigma / sqrt(n)  (standard error)<br><br>As n increases, SE decreases - means concentrate on mu</div>', unsafe_allow_html=True)
        with col2:
            mu_s    = st.slider("Population mu", -5.0, 5.0, 0.0, 0.5, key="samp_mu")
            sigma_s = st.slider("Population sigma", 0.5, 5.0, 2.0, 0.1, key="samp_sig")
            fig = go.Figure()
            x_s = np.linspace(mu_s - 4.5*sigma_s, mu_s + 4.5*sigma_s, 400)
            colors_n = [RS, GD, AC, GR]
            for i, n_s in enumerate([5, 10, 30, 100]):
                se = sigma_s / np.sqrt(n_s)
                y_s = stats.norm.pdf(x_s, mu_s, se)
                fig.add_scatter(x=x_s, y=y_s, mode="lines",
                                line=dict(color=colors_n[i], width=2),
                                name=f"n={n_s}, SE={se:.2f}")
            fig.add_vline(x=mu_s, line_color="white", line_dash="dot", line_width=1.5)
            fig.update_layout(**base_layout(title="Sampling Distribution of X-bar for various n",
                              xaxis_title="X-bar", yaxis_title="Density", height=350,
                              legend=dict(bgcolor="rgba(0,0,0,0)")))
            st.plotly_chart(fig, use_container_width=True)

    with tab_clt:
        st.markdown("**Central Limit Theorem** - Slide 40-41")
        st.markdown("*When n is big enough, the sampling distribution of the mean is approximately Normal - regardless of the parent distribution.*")

        c1, c2, c3 = st.columns(3)
        dist_clt = c1.selectbox("Parent distribution", ["Uniform", "Exponential", "Binomial (p=0.3)", "Bimodal"])
        n_clt    = c2.slider("Sample size n", 1, 100, 30)
        reps_clt = c3.slider("Repetitions", 500, 5000, 2000, 500)

        np.random.seed(42)
        if dist_clt == "Uniform":
            pop = np.random.uniform(0, 1, (reps_clt, n_clt)); mu_t, sig_t = 0.5, np.sqrt(1/12)
        elif dist_clt == "Exponential":
            pop = np.random.exponential(1, (reps_clt, n_clt)); mu_t, sig_t = 1.0, 1.0
        elif dist_clt == "Binomial (p=0.3)":
            pop = np.random.binomial(1, 0.3, (reps_clt, n_clt)); mu_t, sig_t = 0.3, np.sqrt(0.3*0.7)
        else:
            mix = (np.random.random((reps_clt, n_clt)) > 0.5)
            pop = np.where(mix, np.random.normal(3, .5, (reps_clt, n_clt)),
                               np.random.normal(-3, .5, (reps_clt, n_clt)))
            mu_t, sig_t = 0.0, np.sqrt(9.25)

        sample_means = pop.mean(axis=1)
        se_t = sig_t / np.sqrt(n_clt)

        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=[f"Parent: {dist_clt}", f"Distribution of X-bar (n={n_clt})"])
        fig.add_histogram(x=pop[0], nbinsx=40, marker_color=RS, opacity=0.75,
                          histnorm="probability density", row=1, col=1)
        fig.add_histogram(x=sample_means, nbinsx=60, marker_color=AC, opacity=0.75,
                          histnorm="probability density", row=1, col=2)
        xn = np.linspace(sample_means.min(), sample_means.max(), 300)
        fig.add_scatter(x=xn, y=stats.norm.pdf(xn, mu_t, se_t), mode="lines",
                        line=dict(color=GR, width=2.5), name="N(mu, sigma/sqrt(n))", row=1, col=2)
        fig.update_layout(**base_layout(title="Central Limit Theorem", height=380,
                          legend=dict(bgcolor="rgba(0,0,0,0)")))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<div class="pill-row"><div class="pill">True mu = <b>{mu_t:.3f}</b></div><div class="pill">SE = sigma/sqrt(n) = <b>{se_t:.4f}</b></div><div class="pill">Observed mean of X-bar = <b>{sample_means.mean():.4f}</b></div><div class="pill">Observed std of X-bar = <b>{sample_means.std():.4f}</b></div></div>', unsafe_allow_html=True)

    with tab_other:
        st.markdown("**Slide 41 - Other Sampling Distributions**")
        st.markdown("Three distributions used in hypothesis testing: t, F, and chi-square. In Python (scipy.stats) they are `t`, `f`, and `chi2`.")
        dist_o = st.selectbox("Distribution", ["t-distribution", "F-distribution", "Chi-Square"])

        if dist_o == "t-distribution":
            df_t = st.slider("Degrees of freedom (df)", 1, 50, 10)
            x_t  = np.linspace(-5, 5, 400)
            fig = go.Figure()
            fig.add_scatter(x=x_t, y=stats.norm.pdf(x_t), line=dict(color=GRID, width=1.5, dash="dot"), name="N(0,1)")
            fig.add_scatter(x=x_t, y=stats.t.pdf(x_t, df_t), fill="tozeroy",
                            fillcolor="rgba(92,124,250,0.15)", line=dict(color=AC, width=2.5),
                            name=f"t(df={df_t})")
            fig.update_layout(**base_layout(title=f"t-distribution (df={df_t}) vs Normal",
                              xaxis_title="x", yaxis_title="Density", height=340,
                              legend=dict(bgcolor="rgba(0,0,0,0)")))
            st.plotly_chart(fig, use_container_width=True)
            st.info("As df increases, the t-distribution converges to N(0,1). Heavier tails for small samples.")
            st.markdown('<div class="formula">from scipy.stats import t<br>t.ppf(0.975, df=10)  # critical value<br>t.cdf(2.0,  df=10)   # p-value</div>', unsafe_allow_html=True)

        elif dist_o == "F-distribution":
            c1, c2 = st.columns(2)
            df1 = c1.slider("df1 (sample 1)", 1, 50, 10)
            df2 = c2.slider("df2 (sample 2)", 1, 100, 30)
            x_f2 = np.linspace(0.01, 5, 400)
            fig = go.Figure()
            fig.add_scatter(x=x_f2, y=stats.f.pdf(x_f2, df1, df2), fill="tozeroy",
                            fillcolor="rgba(56,217,169,0.15)", line=dict(color=GR, width=2.5),
                            name=f"F({df1},{df2})")
            fig.update_layout(**base_layout(title=f"F-distribution (df1={df1}, df2={df2})",
                              xaxis_title="x", yaxis_title="Density", height=340,
                              legend=dict(bgcolor="rgba(0,0,0,0)")))
            st.plotly_chart(fig, use_container_width=True)
            st.info("F-distribution tests two samples, so two degrees of freedom are specified: df1 and df2.")

        else:
            df_c = st.slider("Degrees of freedom (df)", 1, 30, 5)
            x_c  = np.linspace(0.01, 40, 400)
            fig = go.Figure()
            fig.add_scatter(x=x_c, y=stats.chi2.pdf(x_c, df_c), fill="tozeroy",
                            fillcolor="rgba(255,212,59,0.15)", line=dict(color=GD, width=2.5),
                            name=f"chi2(df={df_c})")
            fig.update_layout(**base_layout(title=f"Chi-Square distribution (df={df_c})",
                              xaxis_title="x", yaxis_title="Density", height=340,
                              legend=dict(bgcolor="rgba(0,0,0,0)")))
            st.plotly_chart(fig, use_container_width=True)
            st.info("Chi-square is used for goodness-of-fit and independence tests. Note: scipy uses ddof for 'delta degrees of freedom'.")
            st.markdown('<div class="formula">from scipy.stats import chi2<br>chi2.pdf(x, df=5)   # density<br>chi2.cdf(x, df=5)   # cumulative</div>', unsafe_allow_html=True)
