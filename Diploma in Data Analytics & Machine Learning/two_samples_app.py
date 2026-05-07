import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
from scipy.stats import t, f, chi2, norm
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Lecture 7 · Two-Sample Tests & Goodness of Fit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  :root { --teal:#007BA7; --teal2:#005f7f; --red:#c0392b; }
  .stApp { background: #f9fbfc; }
  h1 { color: var(--teal2) !important; }
  h2 { color: var(--teal) !important; border-bottom:2px solid var(--teal); padding-bottom:4px; }
  .metric-card { background:white; border-left:5px solid var(--teal); border-radius:8px;
    padding:14px 18px; margin:6px 0; box-shadow:0 1px 4px rgba(0,0,0,.08); }
  .metric-card .label { font-size:0.78rem; color:#666; margin-bottom:2px; }
  .metric-card .value { font-size:1.3rem; font-weight:700; color:var(--teal2); }
  .verdict-reject { background:#fde8e8; border-left:5px solid var(--red); border-radius:8px;
    padding:14px 18px; margin-top:10px; font-weight:600; color:var(--red); }
  .verdict-fail { background:#e8f8e8; border-left:5px solid #27ae60; border-radius:8px;
    padding:14px 18px; margin-top:10px; font-weight:600; color:#1e8449; }
  .info-box { background:#e8f4fb; border-left:5px solid var(--teal); border-radius:8px;
    padding:12px 16px; margin:8px 0; font-size:0.93rem; color:#1a3a4a; }
  .formula-box { background:#fff8e1; border-left:5px solid #f39c12; border-radius:8px;
    padding:12px 16px; margin:8px 0; font-family:monospace; font-size:0.93rem; }
  section[data-testid="stSidebar"] { background: var(--teal2) !important; }
  section[data-testid="stSidebar"] * { color: white !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 📊 Lecture 7")
    st.markdown("**Data Analytics**")
    st.markdown("**Fitzwilliam Institute**")
    st.markdown("---")
    section = st.radio("Navigate", [
        "🏠 Overview",
        "🔬 Fisher's F-Test",
        "📐 Independent t-Test",
        "🔗 Paired t-Test",
        "🎲 Goodness of Fit (χ²)",
        "🧪 Full Worked Example",
    ])
    st.markdown("---")
    st.markdown("*April 23, 2026*")

# ─── shared data ──────────────────────────────────────────────────────────────
mpg_auto   = np.array([21.4,18.7,18.1,14.3,24.4,22.8,19.2,17.8,16.4,17.3,15.2,10.4,10.4,14.7,21.5,15.5,15.2,13.3,19.2])
mpg_manual = np.array([21.0,21.0,22.8,32.4,30.4,33.9,21.5,15.5,15.2,13.3,27.3,26.0,30.4])

# ═══════════════════════════════════════════════════════════════════════════════
if section == "🏠 Overview":
    st.title("Lecture 7 · Comparing Two Population Means & Goodness of Fit")
    st.markdown("**Data Analytics - Fitzwilliam Institute · Deepak John Reji**")
    st.divider()

    col1, col2, col3 = st.columns(3)
    for col, title, body in zip([col1,col2,col3],
        ["Independent Samples","Paired Samples","Goodness of Fit"],
        ["Compare two unrelated groups using pooled or separate variances",
         "Compare matched pairs - before/after or same subjects twice",
         "Test whether observed categorical data matches expected proportions"]):
        with col:
            st.markdown(f'<div class="metric-card"><div class="label">Topic</div>'
                        f'<div class="value">{title}</div>'
                        f'<div class="label" style="margin-top:6px">{body}</div></div>',
                        unsafe_allow_html=True)

    st.divider()
    st.subheader("🗺️ Decision Tree: Which Test?")

    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.set_xlim(0,10); ax.set_ylim(-0.5, 7); ax.axis('off')

    nodes = [
        (5.0, 6.5, 2.2, 0.55, "What type of data?", "#007BA7"),
        (2.0, 5.2, 2.0, 0.55, "Categorical", "#8e44ad"),
        (8.0, 5.2, 2.0, 0.55, "Numerical", "#2980b9"),
        (2.0, 3.8, 2.0, 0.55, "Goodness of\nFit (χ²)", "#c0392b"),
        (6.5, 3.8, 2.0, 0.55, "Independent?", "#2980b9"),
        (9.2, 3.8, 1.6, 0.55, "Paired\nt-Test", "#27ae60"),
        (4.5, 2.3, 2.0, 0.55, "Equal\nVariances?\n(Fisher F)", "#e67e22"),
        (8.2, 2.3, 2.0, 0.55, "Welch\nt-Test", "#c0392b"),
        (2.5, 0.8, 2.0, 0.55, "Pooled\nt-Test", "#27ae60"),
        (6.5, 0.8, 2.0, 0.55, "Unequal →\nWelch", "#c0392b"),
    ]
    for (x,y,w,h,txt,c) in nodes:
        p = mpatches.FancyBboxPatch((x-w/2,y-h/2),w,h,
            boxstyle="round,pad=0.06",facecolor=c,edgecolor='white',lw=2)
        ax.add_patch(p)
        ax.text(x,y,txt,ha='center',va='center',fontsize=8,color='white',
                fontweight='bold',multialignment='center')

    arrs = [
        (5.0,6.2, 2.0,5.5, "Categorical"),
        (5.0,6.2, 8.0,5.5, "Numerical"),
        (2.0,4.9, 2.0,4.1, ""),
        (8.0,4.9, 7.5,4.1, "Yes"),
        (8.0,4.9, 9.2,4.1, "No"),
        (7.5,3.5, 5.5,2.6, "Yes"),
        (7.5,3.5, 8.2,2.6, "No→Welch"),
        (5.5,2.0, 3.5,1.1, "Equal"),
        (5.5,2.0, 6.5,1.1, "Unequal"),
    ]
    for (x1,y1,x2,y2,lbl) in arrs:
        ax.annotate("",xy=(x2,y2),xytext=(x1,y1),
            arrowprops=dict(arrowstyle="->",color='#444',lw=1.5))
        if lbl:
            ax.text((x1+x2)/2+0.05,(y1+y2)/2+0.05,lbl,fontsize=7.5,color='#333')

    plt.tight_layout(); st.pyplot(fig); plt.close()

    st.markdown("""<div class="info-box">
💡 <b>Key rule:</b> For independent samples, always run <b>Fisher's F-test first</b> 
to decide between pooled (equal variances) and Welch (unequal variances) t-test.
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
elif section == "🔬 Fisher's F-Test":
    st.title("🔬 Fisher's F-Test")
    st.markdown("**Test whether two population variances are equal**")
    st.divider()

    col_info, col_play = st.columns([1, 1.5])

    with col_info:
        st.subheader("Concept")
        st.markdown("""<div class="info-box">
• H₀: σ₁² = σ₂²<br>
• H₁: σ₁² ≠ σ₂²<br><br>
Compare the <b>ratio</b> of sample variances.<br>
If equal, ratio ≈ 1.
</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="formula-box">
F = s_larger² / s_smaller²

df₁ = n_larger − 1
df₂ = n_smaller − 1

If p &lt; α → variances differ
         → use Welch t-test

If p ≥ α → variances equal
         → use pooled t-test
</div>""", unsafe_allow_html=True)

    with col_play:
        st.subheader("🎮 Interactive Explorer")
        s1 = st.slider("s₁ (Std Dev group 1)", 0.5, 10.0, 3.83, 0.1)
        s2 = st.slider("s₂ (Std Dev group 2)", 0.5, 10.0, 6.17, 0.1)
        n1_f = st.slider("n₁", 5, 100, 19)
        n2_f = st.slider("n₂", 5, 100, 13)
        alpha_f = st.select_slider("α", [0.01, 0.05, 0.10], value=0.05, key="af")

        v1, v2 = s1**2, s2**2
        if v1 >= v2:
            F_r = v1/v2; df1,df2 = n1_f-1,n2_f-1
        else:
            F_r = v2/v1; df1,df2 = n2_f-1,n1_f-1

        p_fv = 2 * f.sf(F_r, df1, df2)
        c1,c2,c3 = st.columns(3)
        c1.metric("F-ratio", f"{F_r:.4f}")
        c2.metric("p-value", f"{p_fv:.4f}")
        c3.metric("df", f"{df1}, {df2}")

        if p_fv < alpha_f:
            st.markdown(f'<div class="verdict-reject">❌ p={p_fv:.4f} &lt; α={alpha_f} → Variances DIFFER → Use <b>Welch</b> t-test</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="verdict-fail">✅ p={p_fv:.4f} ≥ α={alpha_f} → Variances EQUAL → Use <b>pooled</b> t-test</div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("📈 Visualisation")
    fig, axes = plt.subplots(1, 2, figsize=(12,4))

    x_max = max(8, F_r*1.6)
    x_fplot = np.linspace(0.01, x_max, 500)
    y_fplot = f.pdf(x_fplot, df1, df2)
    crit_fp = f.ppf(1-alpha_f/2, df1, df2)

    axes[0].plot(x_fplot, y_fplot, '#007BA7', lw=2)
    axes[0].fill_between(x_fplot, y_fplot, where=(x_fplot>=crit_fp), color='#e74c3c', alpha=0.35, label=f'Rejection region')
    axes[0].axvline(F_r, color='#e67e22', lw=2.5, linestyle='--', label=f'F={F_r:.3f}')
    axes[0].axvline(crit_fp, color='#e74c3c', lw=1.5, linestyle=':', label=f'Critical={crit_fp:.3f}')
    axes[0].set_xlabel('F'); axes[0].set_ylabel('Density')
    axes[0].set_title(f'F-Distribution (df={df1},{df2})', fontweight='bold')
    axes[0].legend(fontsize=8); axes[0].spines[['top','right']].set_visible(False)

    bars = axes[1].bar(['s₁²={:.2f}'.format(v1),'s₂²={:.2f}'.format(v2)],
                       [v1,v2], color=['#007BA7','#2ecc71'], width=0.5, edgecolor='white')
    axes[1].set_ylabel('Variance (s²)'); axes[1].set_title('Variance Comparison', fontweight='bold')
    for bar,val in zip(bars,[v1,v2]):
        axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1, f'{val:.2f}',
                     ha='center', fontweight='bold')
    axes[1].spines[['top','right']].set_visible(False)
    plt.tight_layout(); st.pyplot(fig); plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
elif section == "📐 Independent t-Test":
    st.title("📐 Two-Sample t-Test: Independent Samples")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["📚 Theory & Formulas", "🎮 Interactive Calculator", "🚗 mtcars Example"])

    with tab1:
        cola, colb = st.columns(2)
        with cola:
            st.subheader("Pooled Variance t-Test")
            st.markdown('<div class="info-box">Use when: <b>variances are equal</b> (F-test p ≥ α)</div>', unsafe_allow_html=True)
            st.markdown("""<div class="formula-box">
Pooled SD:
  s_p = √[((n₁-1)s₁² + (n₂-1)s₂²) / (n₁+n₂-2)]

SE = s_p × √(1/n₁ + 1/n₂)

t = (x̄₁ - x̄₂) / SE

df = n₁ + n₂ - 2

CI: (x̄₁-x̄₂) ± t* × SE
</div>""", unsafe_allow_html=True)

        with colb:
            st.subheader("Welch t-Test (Unequal Variances)")
            st.markdown('<div class="info-box">Use when: <b>variances differ</b> (F-test p &lt; α)</div>', unsafe_allow_html=True)
            st.markdown("""<div class="formula-box">
SE = √(s₁²/n₁ + s₂²/n₂)

t = (x̄₁ - x̄₂) / SE

Welch df (Satterthwaite):
  df = (s₁²/n₁ + s₂²/n₂)²
     / [(s₁²/n₁)²/(n₁-1) + (s₂²/n₂)²/(n₂-1)]

CI: (x̄₁-x̄₂) ± t* × SE
</div>""", unsafe_allow_html=True)

    with tab2:
        st.subheader("🎮 Two-Sample t-Test Calculator")
        c1,c2 = st.columns(2)
        with c1:
            st.markdown("**Group 1**")
            m1 = st.number_input("Mean x̄₁", value=17.15)
            sd1 = st.number_input("SD s₁", value=3.83, min_value=0.01)
            n1i = st.number_input("n₁", value=19, min_value=2)
        with c2:
            st.markdown("**Group 2**")
            m2 = st.number_input("Mean x̄₂", value=24.39)
            sd2 = st.number_input("SD s₂", value=6.17, min_value=0.01)
            n2i = st.number_input("n₂", value=13, min_value=2)

        c3,c4 = st.columns(2)
        with c3:
            alpha_t = st.select_slider("α", [0.01,0.05,0.10], value=0.05, key="at")
            tail_t = st.radio("Hypothesis", ["Two-tailed","Left (μ₁<μ₂)","Right (μ₁>μ₂)"])
        with c4:
            veq = st.radio("Variance", ["Pooled (equal)","Welch (unequal)"])

        diff_t = m1 - m2
        if "Pooled" in veq:
            sp2 = ((n1i-1)*sd1**2 + (n2i-1)*sd2**2)/(n1i+n2i-2)
            se_t = np.sqrt(sp2)*np.sqrt(1/n1i+1/n2i)
            df_t = n1i+n2i-2; method_t="Pooled"
        else:
            se_t = np.sqrt(sd1**2/n1i + sd2**2/n2i)
            num = (sd1**2/n1i+sd2**2/n2i)**2
            den = (sd1**2/n1i)**2/(n1i-1)+(sd2**2/n2i)**2/(n2i-1)
            df_t = num/den; method_t="Welch"

        t_t = diff_t/se_t
        t_crit_t = t.ppf(1-alpha_t/2, df_t)
        if "Two" in tail_t: p_t = 2*t.sf(abs(t_t),df_t)
        elif "Left" in tail_t: p_t = t.cdf(t_t,df_t)
        else: p_t = t.sf(t_t,df_t)

        ci_tl = diff_t - t_crit_t*se_t
        ci_th = diff_t + t_crit_t*se_t

        st.divider()
        st.subheader(f"Results - {method_t} t-Test")
        r1,r2,r3,r4 = st.columns(4)
        r1.metric("x̄₁−x̄₂", f"{diff_t:.4f}")
        r2.metric("t-stat", f"{t_t:.4f}")
        r3.metric("p-value", f"{p_t:.5f}")
        r4.metric("df", f"{df_t:.1f}")
        st.markdown(f"**95% CI:** ({ci_tl:.4f}, {ci_th:.4f})")

        if p_t < alpha_t:
            st.markdown(f'<div class="verdict-reject">❌ Reject H₀ - Significant difference (p={p_t:.5f} &lt; {alpha_t})</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="verdict-fail">✅ Fail to reject H₀ - No significant difference (p={p_t:.5f} ≥ {alpha_t})</div>', unsafe_allow_html=True)

        fig,ax = plt.subplots(figsize=(10,4))
        xr = np.linspace(-5,5,400); yr = t.pdf(xr,df_t)
        ax.plot(xr,yr,'#007BA7',lw=2)
        if "Two" in tail_t: ax.fill_between(xr,yr,where=(np.abs(xr)>=t_crit_t),color='#e74c3c',alpha=0.3,label='Rejection region')
        elif "Left" in tail_t: ax.fill_between(xr,yr,where=(xr<=t.ppf(alpha_t,df_t)),color='#e74c3c',alpha=0.3,label='Rejection region')
        else: ax.fill_between(xr,yr,where=(xr>=t_crit_t),color='#e74c3c',alpha=0.3,label='Rejection region')
        ax.axvline(t_t,color='#e67e22',lw=2.5,linestyle='--',label=f't={t_t:.3f}')
        ax.set_title(f't-Distribution (df={df_t:.1f}) - {method_t}',fontweight='bold')
        ax.legend(); ax.spines[['top','right']].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()

    with tab3:
        st.subheader("🚗 mtcars: Manual vs Automatic MPG")
        ca, cm = st.columns(2)
        with ca:
            st.markdown(f'<div class="metric-card"><div class="label">Automatic (n=19)</div>'
                        f'<div class="value">μ = {np.mean(mpg_auto):.2f} mpg</div>'
                        f'<div class="label">s = {np.std(mpg_auto,ddof=1):.2f}</div></div>', unsafe_allow_html=True)
        with cm:
            st.markdown(f'<div class="metric-card"><div class="label">Manual (n=13)</div>'
                        f'<div class="value">μ = {np.mean(mpg_manual):.2f} mpg</div>'
                        f'<div class="label">s = {np.std(mpg_manual,ddof=1):.2f}</div></div>', unsafe_allow_html=True)

        va = np.var(mpg_auto,ddof=1); vm = np.var(mpg_manual,ddof=1)
        F_m = vm/va; df1m,df2m = len(mpg_manual)-1,len(mpg_auto)-1
        p_fm = 2*f.sf(F_m,df1m,df2m)
        st.markdown(f"**Fisher's F-Test:** F={F_m:.4f}, p={p_fm:.4f}")
        st.markdown('<div class="verdict-fail">✅ p=0.067 > 0.05 → Equal variances → Use pooled t-test</div>', unsafe_allow_html=True)

        t_mc,p_mc = stats.ttest_ind(mpg_auto,mpg_manual,equal_var=True)
        df_mc=len(mpg_auto)+len(mpg_manual)-2
        sp_mc=np.sqrt(((len(mpg_auto)-1)*va+(len(mpg_manual)-1)*vm)/df_mc)
        se_mc=sp_mc*np.sqrt(1/len(mpg_auto)+1/len(mpg_manual))
        d_mc=np.mean(mpg_auto)-np.mean(mpg_manual)
        tc_mc=t.ppf(0.975,df_mc)
        st.markdown(f"**Pooled t-Test:** t={t_mc:.4f}, df={df_mc}, p={p_mc:.6f}")
        st.markdown(f"**95% CI:** ({d_mc-tc_mc*se_mc:.4f}, {d_mc+tc_mc*se_mc:.4f})")
        st.markdown('<div class="verdict-reject">❌ p=0.000285 ≪ 0.05 → Manual transmission cars get significantly better mileage!</div>', unsafe_allow_html=True)

        fig,axes = plt.subplots(1,2,figsize=(12,5))
        axes[0].boxplot([mpg_auto,mpg_manual],labels=['Automatic','Manual'],
            patch_artist=True, boxprops=dict(facecolor='#007BA7',alpha=0.7),
            medianprops=dict(color='white',linewidth=2))
        axes[0].set_ylabel('MPG'); axes[0].set_title('MPG by Transmission',fontweight='bold')
        axes[0].spines[['top','right']].set_visible(False)

        xp=np.linspace(-6,6,400)
        axes[1].plot(xp,t.pdf(xp,df_mc),'#007BA7',lw=2)
        tc_plt=t.ppf(0.975,df_mc)
        axes[1].fill_between(xp,t.pdf(xp,df_mc),where=(np.abs(xp)>=tc_plt),color='#e74c3c',alpha=0.3,label='Rejection region')
        axes[1].axvline(t_mc,color='#e67e22',lw=2.5,linestyle='--',label=f't={t_mc:.3f}')
        axes[1].set_title('t-Test Statistic',fontweight='bold')
        axes[1].legend(); axes[1].spines[['top','right']].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
elif section == "🔗 Paired t-Test":
    st.title("🔗 Paired Samples t-Test")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["📚 Theory", "🎮 Calculator", "💧 Zinc Example"])

    with tab1:
        ca,cb = st.columns(2)
        with ca:
            st.subheader("When are samples paired?")
            st.markdown("""<div class="info-box">
Use paired t-test when observations come in matched pairs:<br><br>
• Before vs after treatment (same subject)<br>
• Two measurements at the same location<br>
• Husband and wife responses<br>
• Left vs right hand measurements
</div>""", unsafe_allow_html=True)
        with cb:
            st.subheader("Formula")
            st.markdown("""<div class="formula-box">
Step 1: Compute differences for each pair
  dᵢ = x₁ᵢ − x₂ᵢ

Step 2: One-sample t-test on differences
  d̄  = mean of dᵢ
  s_d = std dev of dᵢ

  t = d̄ / (s_d / √n)

  df = n − 1

  CI: d̄ ± t* × (s_d / √n)
</div>""", unsafe_allow_html=True)

    with tab2:
        st.subheader("🎮 Paired t-Test Calculator")
        c1,c2 = st.columns(2)
        with c1:
            raw1 = st.text_area("Group 1 / Before",
                "0.430, 0.266, 0.567, 0.531, 0.707, 0.716, 0.651, 0.589, 0.469, 0.723", height=90)
        with c2:
            raw2 = st.text_area("Group 2 / After",
                "0.415, 0.238, 0.390, 0.410, 0.605, 0.609, 0.632, 0.523, 0.411, 0.612", height=90)

        alpha_p2 = st.select_slider("α", [0.01,0.05,0.10], value=0.05, key="ap2")
        tail_p2 = st.radio("Alternative", ["Two-tailed","d̄ > 0","d̄ < 0"])

        try:
            v1p = np.array([float(x.strip()) for x in raw1.split(',')])
            v2p = np.array([float(x.strip()) for x in raw2.split(',')])
            if len(v1p)!=len(v2p):
                st.error("Lists must have equal length!")
            else:
                diffs = v1p - v2p
                db = np.mean(diffs); sd_p = np.std(diffs,ddof=1)
                n_p = len(diffs); se_p = sd_p/np.sqrt(n_p)
                t_p2 = db/se_p; df_p2 = n_p-1
                tc_p2 = t.ppf(1-alpha_p2/2, df_p2)
                if "Two" in tail_p2: pp = 2*t.sf(abs(t_p2),df_p2)
                elif ">" in tail_p2: pp = t.sf(t_p2,df_p2)
                else: pp = t.cdf(t_p2,df_p2)

                r1,r2,r3,r4 = st.columns(4)
                r1.metric("d̄", f"{db:.5f}"); r2.metric("s_d", f"{sd_p:.5f}")
                r3.metric("t", f"{t_p2:.4f}"); r4.metric("p-value", f"{pp:.5f}")
                st.markdown(f"**95% CI:** ({db-tc_p2*se_p:.5f}, {db+tc_p2*se_p:.5f})")

                if pp < alpha_p2:
                    st.markdown(f'<div class="verdict-reject">❌ Reject H₀ - Significant paired difference (p={pp:.5f})</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="verdict-fail">✅ Fail to reject H₀ - No significant difference (p={pp:.5f})</div>', unsafe_allow_html=True)

                fig,axes = plt.subplots(1,3,figsize=(14,4))
                for i,(a,b) in enumerate(zip(v1p,v2p)):
                    col_l = '#e74c3c' if a>b else '#27ae60'
                    axes[0].plot([0,1],[a,b],color=col_l,alpha=0.7,lw=1.5,marker='o',markersize=5)
                axes[0].set_xticks([0,1]); axes[0].set_xticklabels(['Before','After'])
                axes[0].set_title('Paired Observations',fontweight='bold')
                axes[0].spines[['top','right']].set_visible(False)

                cols_d = ['#e74c3c' if d>0 else '#27ae60' for d in diffs]
                axes[1].bar(range(n_p),diffs,color=cols_d,alpha=0.8,edgecolor='white')
                axes[1].axhline(0,color='black',lw=1)
                axes[1].axhline(db,color='#e67e22',lw=2,linestyle='--',label=f'd̄={db:.3f}')
                axes[1].set_title('Differences',fontweight='bold'); axes[1].legend()
                axes[1].spines[['top','right']].set_visible(False)

                xtp = np.linspace(-5,5,400)
                axes[2].plot(xtp,t.pdf(xtp,df_p2),'#007BA7',lw=2)
                axes[2].fill_between(xtp,t.pdf(xtp,df_p2),where=(np.abs(xtp)>=tc_p2),
                                     color='#e74c3c',alpha=0.3,label='Rejection region')
                axes[2].axvline(t_p2,color='#e67e22',lw=2.5,linestyle='--',label=f't={t_p2:.3f}')
                axes[2].set_title('t-Distribution',fontweight='bold'); axes[2].legend(fontsize=8)
                axes[2].spines[['top','right']].set_visible(False)
                plt.tight_layout(); st.pyplot(fig); plt.close()
        except Exception as e:
            st.error(f"Parsing error: {e}")

    with tab3:
        st.subheader("💧 Zinc in Drinking Water")
        st.markdown("""<div class="info-box">
<b>Question:</b> Does zinc concentration in <b>bottom water</b> exceed that of <b>surface water</b>?<br>
H₀: d̄ = 0 &nbsp;|&nbsp; H₁: d̄ > 0 &nbsp;|&nbsp; α = 0.05
</div>""", unsafe_allow_html=True)

        zdf = pd.DataFrame({
            'Location': range(1,11),
            'Bottom':  [0.430,0.266,0.567,0.531,0.707,0.716,0.651,0.589,0.469,0.723],
            'Surface': [0.415,0.238,0.390,0.410,0.605,0.609,0.632,0.523,0.411,0.612]
        })
        zdf['Difference'] = zdf['Bottom'] - zdf['Surface']
        st.dataframe(zdf.style.format({'Bottom':'{:.3f}','Surface':'{:.3f}','Difference':'{:.3f}'}),
                     use_container_width=True)

        dz = zdf['Difference']
        tz = dz.mean()/(dz.std(ddof=1)/np.sqrt(10))
        pz = t.sf(tz, 9)
        r1,r2,r3,r4 = st.columns(4)
        r1.metric("d̄", f"{dz.mean():.5f}"); r2.metric("s_d", f"{dz.std(ddof=1):.5f}")
        r3.metric("t", f"{tz:.4f}"); r4.metric("p (one-tail)", f"{pz:.5f}")
        st.markdown('<div class="verdict-reject">❌ p ≈ 0.0001 ≪ 0.05 → Bottom water zinc IS significantly higher than surface water.</div>', unsafe_allow_html=True)

        fig,axes = plt.subplots(1,2,figsize=(12,4))
        axes[0].plot(zdf['Location'],zdf['Bottom'],'o-',color='#007BA7',label='Bottom',lw=2)
        axes[0].plot(zdf['Location'],zdf['Surface'],'s--',color='#e67e22',label='Surface',lw=2)
        axes[0].set_xlabel('Location'); axes[0].set_ylabel('Zinc Concentration')
        axes[0].set_title('Zinc: Bottom vs Surface by Location',fontweight='bold')
        axes[0].legend(); axes[0].spines[['top','right']].set_visible(False)

        axes[1].bar(zdf['Location'],zdf['Difference'],
                    color=['#e74c3c' if d>0 else '#27ae60' for d in zdf['Difference']],alpha=0.8)
        axes[1].axhline(0,color='black',lw=1)
        axes[1].axhline(dz.mean(),color='#e67e22',lw=2,linestyle='--',label=f'd̄={dz.mean():.4f}')
        axes[1].set_xlabel('Location'); axes[1].set_ylabel('Difference (Bottom−Surface)')
        axes[1].set_title('Differences per Pair',fontweight='bold')
        axes[1].legend(); axes[1].spines[['top','right']].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
elif section == "🎲 Goodness of Fit (χ²)":
    st.title("🎲 Chi-Square Goodness of Fit Test")
    st.divider()

    tab1, tab2, tab3 = st.tabs(["📚 Theory", "🎮 Calculator", "🚬 Smoking Example"])

    with tab1:
        ca,cb = st.columns(2)
        with ca:
            st.subheader("Purpose")
            st.markdown("""<div class="info-box">
Test whether <b>observed frequencies</b> match <b>expected frequencies</b>
from a theoretical distribution.<br><br>
H₀: Observed matches expected proportions.<br>
H₁: They do not match.<br><br>
⚠️ Requirement: all expected counts ≥ 5
</div>""", unsafe_allow_html=True)
        with cb:
            st.subheader("Formula")
            st.markdown("""<div class="formula-box">
For each category i:
  component = (Oᵢ − Eᵢ)² / Eᵢ

Total statistic:
  χ² = Σ (Oᵢ − Eᵢ)² / Eᵢ

Degrees of freedom:
  df = k − 1

Expected count:
  Eᵢ = n × pᵢ

Reject H₀ if p-value &lt; α
</div>""", unsafe_allow_html=True)

        st.subheader("Chi-Square Distribution Shapes")
        fig,ax = plt.subplots(figsize=(10,4))
        xchi = np.linspace(0.01,30,500)
        for df_c,col in zip([1,2,3,5,10],['#007BA7','#2ecc71','#e67e22','#e74c3c','#8e44ad']):
            ax.plot(xchi,chi2.pdf(xchi,df_c),color=col,lw=2,label=f'df={df_c}')
        ax.set_xlim(0,30); ax.set_xlabel('χ²'); ax.set_ylabel('Density')
        ax.set_title('Chi-Square Distributions',fontweight='bold')
        ax.legend(); ax.spines[['top','right']].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()

    with tab2:
        st.subheader("🎮 Goodness of Fit Calculator")
        n_c = st.slider("Number of categories", 2, 8, 4, key="nc")

        cat_names=[]; obs_c=[]; exp_pc=[]
        for i in range(n_c):
            c1,c2,c3 = st.columns(3)
            with c1: cat_names.append(st.text_input(f"Cat {i+1}", f"Category {i+1}", key=f"cn{i}"))
            with c2: obs_c.append(st.number_input(f"Observed", value=50, min_value=0, key=f"ob{i}"))
            with c3: exp_pc.append(st.number_input(f"Expected %", value=round(100/n_c,1), key=f"ep{i}"))

        alpha_c2 = st.select_slider("α", [0.01,0.05,0.10], value=0.05, key="ac2")

        obs_a = np.array(obs_c); ep_a = np.array(exp_pc)/100
        n_tot = obs_a.sum(); exp_a = ep_a*n_tot

        if abs(ep_a.sum()-1.0)>0.01:
            st.warning(f"Proportions sum to {ep_a.sum()*100:.1f}% - must equal 100%")
        else:
            chi2_c = np.sum((obs_a-exp_a)**2/exp_a)
            p_c2 = chi2.sf(chi2_c, n_c-1)

            rdf = pd.DataFrame({'Category':cat_names,'Observed':obs_a,
                'Expected':np.round(exp_a,2),'(O-E)²/E':np.round((obs_a-exp_a)**2/exp_a,4)})
            st.dataframe(rdf, use_container_width=True)

            r1,r2,r3 = st.columns(3)
            r1.metric("χ²", f"{chi2_c:.4f}"); r2.metric("p-value", f"{p_c2:.5f}"); r3.metric("df", f"{n_c-1}")

            if p_c2 < alpha_c2:
                st.markdown(f'<div class="verdict-reject">❌ Reject H₀ - Observed does NOT match expected (p={p_c2:.5f})</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="verdict-fail">✅ Fail to reject H₀ - Observed is consistent with expected (p={p_c2:.5f})</div>', unsafe_allow_html=True)

            fig,axes = plt.subplots(1,2,figsize=(12,4))
            xp2 = np.arange(n_c)
            axes[0].bar(xp2-0.2,obs_a,0.4,label='Observed',color='#007BA7',alpha=0.85)
            axes[0].bar(xp2+0.2,exp_a,0.4,label='Expected',color='#e67e22',alpha=0.85)
            axes[0].set_xticks(xp2); axes[0].set_xticklabels(cat_names,rotation=15)
            axes[0].set_title('Observed vs Expected',fontweight='bold')
            axes[0].legend(); axes[0].spines[['top','right']].set_visible(False)

            x_chi2p = np.linspace(0.01,max(chi2_c*2,chi2.ppf(0.999,n_c-1)),400)
            y_chi2p = chi2.pdf(x_chi2p,n_c-1)
            crit_c2 = chi2.ppf(1-alpha_c2,n_c-1)
            axes[1].plot(x_chi2p,y_chi2p,'#007BA7',lw=2)
            axes[1].fill_between(x_chi2p,y_chi2p,where=(x_chi2p>=crit_c2),
                                 color='#e74c3c',alpha=0.3,label='Rejection region')
            axes[1].axvline(chi2_c,color='#e67e22',lw=2.5,linestyle='--',label=f'χ²={chi2_c:.3f}')
            axes[1].set_title(f'χ²-Distribution (df={n_c-1})',fontweight='bold')
            axes[1].legend(fontsize=8); axes[1].spines[['top','right']].set_visible(False)
            plt.tight_layout(); st.pyplot(fig); plt.close()

    with tab3:
        st.subheader("🚬 Student Smoking Survey")
        st.markdown("""<div class="info-box">
237 Statistics students at University of Adelaide.<br>
<b>Question:</b> Does the sample match campus-wide smoking statistics at α=0.05?
</div>""", unsafe_allow_html=True)
        smoke_obs = np.array([11,189,19,17])
        smoke_ep  = np.array([0.045,0.795,0.085,0.075])
        cats_s    = ['Heavy','Never','Occas','Regul']
        n_s = smoke_obs.sum(); smoke_exp = smoke_ep*n_s

        sdf = pd.DataFrame({'Category':cats_s,'Expected %':[f'{p*100}%' for p in smoke_ep],
            'Expected Count':np.round(smoke_exp,2),'Observed':smoke_obs,
            '(O-E)²/E':np.round((smoke_obs-smoke_exp)**2/smoke_exp,4)})
        st.dataframe(sdf, use_container_width=True)

        chi2_s = np.sum((smoke_obs-smoke_exp)**2/smoke_exp)
        p_s = chi2.sf(chi2_s,3)
        r1,r2 = st.columns(2)
        r1.metric("χ²", f"{chi2_s:.4f}"); r2.metric("p-value", f"{p_s:.4f}")
        st.markdown('<div class="verdict-fail">✅ p = 0.991 > 0.05 → The sample IS consistent with campus smoking statistics.</div>', unsafe_allow_html=True)

        fig,axes = plt.subplots(1,2,figsize=(12,4))
        xs2 = np.arange(4)
        axes[0].bar(xs2-0.2,smoke_obs,0.4,label='Observed',color='#007BA7',alpha=0.85)
        axes[0].bar(xs2+0.2,smoke_exp,0.4,label='Expected',color='#e67e22',alpha=0.85)
        axes[0].set_xticks(xs2); axes[0].set_xticklabels(cats_s)
        axes[0].set_title('Smoking: Observed vs Expected',fontweight='bold')
        axes[0].legend(); axes[0].spines[['top','right']].set_visible(False)

        xc2s = np.linspace(0.01,15,400)
        axes[1].plot(xc2s,chi2.pdf(xc2s,3),'#007BA7',lw=2)
        crits = chi2.ppf(0.95,3)
        axes[1].fill_between(xc2s,chi2.pdf(xc2s,3),where=(xc2s>=crits),
                              color='#e74c3c',alpha=0.3,label='Rejection region')
        axes[1].axvline(chi2_s,color='#27ae60',lw=2.5,linestyle='--',label=f'χ²={chi2_s:.4f}')
        axes[1].set_title('χ²-Distribution (df=3)',fontweight='bold')
        axes[1].legend(fontsize=8); axes[1].spines[['top','right']].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()

# ═══════════════════════════════════════════════════════════════════════════════
elif section == "🧪 Full Worked Example":
    st.title("🧪 Step-by-Step Worked Example")
    st.markdown("**Full workflow: mtcars MPG analysis**")
    st.divider()

    step = st.radio("Select Step", [
        "Step 1 · State the Problem",
        "Step 2 · Check Normality (QQ Plot)",
        "Step 3 · Fisher's F-Test",
        "Step 4 · Pooled t-Test",
        "Step 5 · Conclusion",
        "📋 All Tests Summary",
    ])

    if "Step 1" in step:
        st.subheader("Step 1: State the Problem")
        st.markdown("""<div class="info-box">
<b>Dataset:</b> mtcars - 32 cars from 1974 Motor Trend<br><br>
<b>Question:</b> Is there a difference in mean mpg between automatic and manual transmission?<br><br>
H₀: μ_auto = μ_manual<br>
H₁: μ_auto ≠ μ_manual<br><br>
α = 0.05 &nbsp;|&nbsp; n_auto = 19 &nbsp;|&nbsp; n_manual = 13<br><br>
⚠️ Both < 30 → must verify normality!
</div>""", unsafe_allow_html=True)
        fig,ax = plt.subplots(figsize=(8,4))
        ax.hist(mpg_auto,bins=8,alpha=0.7,color='#007BA7',label='Automatic',edgecolor='white')
        ax.hist(mpg_manual,bins=6,alpha=0.7,color='#e67e22',label='Manual',edgecolor='white')
        ax.set_xlabel('MPG'); ax.set_ylabel('Count')
        ax.set_title('Distribution of MPG by Transmission',fontweight='bold')
        ax.legend(); ax.spines[['top','right']].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()

    elif "Step 2" in step:
        st.subheader("Step 2: Check Normality - QQ Plots")
        st.markdown("""<div class="info-box">
A <b>Normal QQ plot</b> plots sample quantiles against theoretical normal quantiles.
If points follow the diagonal, the data is approximately normal.
</div>""", unsafe_allow_html=True)
        fig,axes = plt.subplots(1,2,figsize=(12,5))
        for ax,data,label,col in zip(axes,[mpg_auto,mpg_manual],['Automatic','Manual'],['#007BA7','#e67e22']):
            (osm,osr),(slope,intercept,r) = stats.probplot(data)
            ax.scatter(osm,osr,color=col,s=60,zorder=3)
            lx = np.array([min(osm),max(osm)])
            ax.plot(lx,slope*lx+intercept,'k--',lw=1.5,label=f'r²={r**2:.3f}')
            ax.set_xlabel('Theoretical Quantiles'); ax.set_ylabel('Sample Quantiles')
            ax.set_title(f'QQ Plot - {label} (n={len(data)})',fontweight='bold')
            ax.legend(); ax.spines[['top','right']].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()
        st.markdown('<div class="verdict-fail">✅ Both plots roughly follow the diagonal → Normality assumption is reasonable.</div>', unsafe_allow_html=True)

    elif "Step 3" in step:
        st.subheader("Step 3: Fisher's F-Test for Variance Equality")
        va=np.var(mpg_auto,ddof=1); vm=np.var(mpg_manual,ddof=1)
        F3=vm/va; df1_3,df2_3=len(mpg_manual)-1,len(mpg_auto)-1
        p3=2*f.sf(F3,df1_3,df2_3)
        st.markdown(f"""<div class="formula-box">
s²_auto   = {va:.4f}
s²_manual = {vm:.4f}

F = s²_manual / s²_auto = {vm:.4f} / {va:.4f} = {F3:.4f}
df₁ = {df1_3},  df₂ = {df2_3}
p-value (two-tailed) = {p3:.5f}
</div>""", unsafe_allow_html=True)

        fig,ax = plt.subplots(figsize=(9,4))
        xf3=np.linspace(0.01,10,400); yf3=f.pdf(xf3,df1_3,df2_3)
        crit3=f.ppf(0.975,df1_3,df2_3)
        ax.plot(xf3,yf3,'#007BA7',lw=2)
        ax.fill_between(xf3,yf3,where=(xf3>=crit3),color='#e74c3c',alpha=0.3,label='Rejection region (α/2=0.025)')
        ax.axvline(F3,color='#e67e22',lw=2.5,linestyle='--',label=f'F={F3:.3f}')
        ax.set_title(f'F-Distribution (df={df1_3},{df2_3})',fontweight='bold')
        ax.legend(); ax.spines[['top','right']].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()
        st.markdown(f'<div class="verdict-fail">✅ p={p3:.4f} > 0.05 → Variances are equal → proceed with <b>pooled t-test</b></div>', unsafe_allow_html=True)

    elif "Step 4" in step:
        st.subheader("Step 4: Pooled Two-Sample t-Test")
        va=np.var(mpg_auto,ddof=1); vm=np.var(mpg_manual,ddof=1)
        na,nm=len(mpg_auto),len(mpg_manual)
        sp2=((na-1)*va+(nm-1)*vm)/(na+nm-2); sp=np.sqrt(sp2)
        se4=sp*np.sqrt(1/na+1/nm)
        d4=np.mean(mpg_auto)-np.mean(mpg_manual); t4=d4/se4; df4=na+nm-2
        p4=2*t.sf(abs(t4),df4); tc4=t.ppf(0.975,df4)
        st.markdown(f"""<div class="formula-box">
s_p² = [(19-1)×{va:.4f} + (13-1)×{vm:.4f}] / (19+13-2)
     = {sp2:.4f}   →   s_p = {sp:.4f}

SE = {sp:.4f} × √(1/19 + 1/13) = {se4:.4f}

t = ({np.mean(mpg_auto):.5f} − {np.mean(mpg_manual):.5f}) / {se4:.4f}
  = {t4:.4f}

df = 19 + 13 − 2 = 30
p-value = {p4:.6f}
95% CI: ({d4-tc4*se4:.4f},  {d4+tc4*se4:.4f})
</div>""", unsafe_allow_html=True)

        fig,axes=plt.subplots(1,2,figsize=(12,4))
        xg=np.linspace(5,45,200)
        axes[0].plot(xg,norm.pdf(xg,np.mean(mpg_auto),np.sqrt(va)),'#007BA7',lw=2,label=f'Auto μ={np.mean(mpg_auto):.1f}')
        axes[0].plot(xg,norm.pdf(xg,np.mean(mpg_manual),np.sqrt(vm)),'#e67e22',lw=2,label=f'Manual μ={np.mean(mpg_manual):.1f}')
        axes[0].set_xlabel('MPG'); axes[0].set_title('Sampling Distributions',fontweight='bold')
        axes[0].legend(); axes[0].spines[['top','right']].set_visible(False)

        xtp=np.linspace(-6,6,400); tc_p=t.ppf(0.975,30)
        axes[1].plot(xtp,t.pdf(xtp,30),'#007BA7',lw=2)
        axes[1].fill_between(xtp,t.pdf(xtp,30),where=(np.abs(xtp)>=tc_p),color='#e74c3c',alpha=0.3)
        axes[1].axvline(t4,color='#e67e22',lw=2.5,linestyle='--',label=f't={t4:.3f}')
        axes[1].set_title('t-Distribution (df=30)',fontweight='bold')
        axes[1].legend(); axes[1].spines[['top','right']].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()
        st.markdown(f'<div class="verdict-reject">❌ t={t4:.4f}, p={p4:.6f} ≪ 0.05 → Reject H₀</div>', unsafe_allow_html=True)

    elif "Step 5" in step:
        st.subheader("Step 5: Conclusion")
        st.markdown("""<div class="info-box">
<b>Statistical conclusion:</b> We reject H₀. There is a statistically significant
difference in mpg between automatic and manual transmission (t=−4.106, df=30, p=0.000285).<br><br>
<b>Effect:</b><br>
• Automatic mean: 17.15 mpg<br>
• Manual mean: 24.39 mpg<br>
• Difference: ~7.24 mpg in favour of manual<br>
• 95% CI: automatic gets between 3.64 and 10.85 mpg less than manual<br><br>
<b>Caveat:</b> Observational data - other variables (weight, cylinders) are confounded.
</div>""", unsafe_allow_html=True)

        fig,ax=plt.subplots(figsize=(8,5))
        means=[np.mean(mpg_auto),np.mean(mpg_manual)]
        sems=[stats.sem(mpg_auto),stats.sem(mpg_manual)]
        bars=ax.bar(['Automatic','Manual'],means,color=['#007BA7','#e67e22'],
                    width=0.5,edgecolor='white',lw=2,alpha=0.9)
        ax.errorbar(['Automatic','Manual'],means,yerr=[1.96*s for s in sems],
                    fmt='none',color='black',capsize=8,capthick=2,lw=2)
        for bar,m in zip(bars,means):
            ax.text(bar.get_x()+bar.get_width()/2,m+0.3,f'{m:.2f} mpg',
                    ha='center',fontweight='bold',color='#333')
        ax.annotate('',xy=(1,27),xytext=(0,27),arrowprops=dict(arrowstyle='<->',color='black',lw=1.5))
        ax.text(0.5,27.5,f'Δ={means[1]-means[0]:.2f} mpg\np < 0.001',ha='center',fontsize=10)
        ax.set_ylabel('Mean MPG'); ax.set_ylim(0,33)
        ax.set_title('Mean MPG by Transmission Type',fontweight='bold')
        ax.spines[['top','right']].set_visible(False)
        plt.tight_layout(); st.pyplot(fig); plt.close()

    else:
        st.subheader("📋 All Tests: Quick Reference")
        sumdf = pd.DataFrame({
            'Test':['Fisher F-Test','Pooled t-Test','Welch t-Test','Paired t-Test','Chi-Square GoF'],
            'Use When':['Check variance equality','Independent, equal variances','Independent, unequal variances','Matched/dependent pairs','Categorical vs expected proportions'],
            'Statistic':['F=s₁²/s₂²','t=Δx̄/(s_p√(1/n₁+1/n₂))','t=Δx̄/√(s₁²/n₁+s₂²/n₂)','t=d̄/(s_d/√n)','χ²=Σ(O-E)²/E'],
            'df':['n₁-1, n₂-1','n₁+n₂-2','Welch-Satterthwaite','n-1','k-1'],
        })
        st.dataframe(sumdf, use_container_width=True)
        st.divider()
        st.subheader("Workflow Checklist")
        for i,(chk,note) in enumerate([
            ("Independent or Paired?","If paired → use paired t-test directly"),
            ("Check normality","QQ plot or Shapiro-Wilk (especially for small samples)"),
            ("Fisher's F-Test","p<α → Welch | p≥α → Pooled"),
            ("Run t-Test","Report t, df, p-value, 95% CI"),
            ("Categorical data?","Chi-Square GoF - ensure all Eᵢ ≥ 5"),
            ("Interpret","Effect size, practical significance, caveats"),
        ],1):
            st.markdown(f'<div class="metric-card"><div class="label">Step {i}</div>'
                        f'<div class="value" style="font-size:0.95rem">{chk}</div>'
                        f'<div class="label" style="margin-top:4px">→ {note}</div></div>',
                        unsafe_allow_html=True)

st.divider()
st.markdown('<div style="text-align:center;color:#aaa;font-size:0.8rem">Lecture 7 · Data Analytics · Fitzwilliam Institute · Deepak John Reji · April 23, 2026</div>', unsafe_allow_html=True)
