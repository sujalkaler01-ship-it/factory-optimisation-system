import streamlit as st

# ------------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Factory Optimisation System",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# CLEAN CORPORATE THEME CSS (shared design system — keep in sync
# across app.py / Dashboard.py / Factory_Optimization.py / etc.)
# ------------------------------------------------------------------
st.markdown("""
<style>
    /* ================= DESIGN TOKENS ================= */
    :root {
        --bg: #f5f7fb;
        --surface: #ffffff;
        --border: #e2e8f0;
        --border-soft: #edf1f7;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --text-muted: #64748b;
        --accent: #2563eb;
        --accent-dark: #1e40af;
        --accent-soft: #eff6ff;
        --accent-soft-2: #dbeafe;
        --success: #16a34a;
        --danger: #dc2626;
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.05);
        --shadow-md: 0 4px 16px rgba(15, 23, 42, 0.06);
        --shadow-hover: 0 8px 24px rgba(37, 99, 235, 0.10);
    }

    /* ================= BASE ================= */
    .stApp {
        background: var(--bg);
    }
    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .fade-in { animation: fadeInUp 0.45s ease both; }

    /* ================= HERO BANNER ================= */
    .hero-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 55%, #3b82f6 100%);
        border-radius: var(--radius-lg);
        padding: 2.2rem 2.4rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 12px 32px rgba(30, 58, 138, 0.22);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::after {
        content: "";
        position: absolute;
        top: -40%; right: -10%;
        width: 320px; height: 320px;
        background: radial-gradient(circle, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
    }
    .hero-icon-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 52px; height: 52px;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: var(--radius-md);
        font-size: 1.6rem;
        margin-bottom: 0.9rem;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0 0 0.35rem 0;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #dbeafe;
        margin: 0;
        position: relative;
        z-index: 1;
        max-width: 640px;
        line-height: 1.5;
    }

    /* ================= SECTION HEADERS ================= */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 2.2rem 0 1rem 0;
    }
    .section-header .badge-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px; height: 30px;
        background: var(--accent-soft);
        border-radius: var(--radius-sm);
        font-size: 0.95rem;
    }

    /* ================= GENERIC CARD ================= */
    .info-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1rem 1.1rem;
        margin-bottom: 0.9rem;
        box-shadow: var(--shadow-sm);
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
        display: flex;
        align-items: center;
        gap: 0.85rem;
    }
    .info-card:hover {
        transform: translateY(-2px);
        border-color: #bfdbfe;
        box-shadow: var(--shadow-hover);
    }
    .info-card .icon-badge {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 38px; height: 38px;
        background: var(--accent-soft);
        border-radius: var(--radius-sm);
        font-size: 1.05rem;
    }
    .info-card .text {
        font-size: 0.92rem;
        color: var(--text-secondary);
        font-weight: 500;
        line-height: 1.4;
    }

    /* ================= FEATURE CARD ================= */
    .feature-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1rem 1.1rem;
        margin-bottom: 0.9rem;
        box-shadow: var(--shadow-sm);
        display: flex;
        align-items: center;
        gap: 0.8rem;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
    }
    .feature-card .icon-badge {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 38px; height: 38px;
        background: var(--accent-dark);
        color: #fff;
        border-radius: var(--radius-sm);
        font-size: 1.05rem;
    }
    .feature-card .text {
        font-size: 0.92rem;
        font-weight: 600;
        color: var(--text-primary);
    }

    /* ================= PANEL ================= */
    .panel {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem 1.7rem;
        box-shadow: var(--shadow-sm);
        margin-bottom: 1rem;
    }
    .panel p, .panel li {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.65;
    }
    .panel ul { margin-bottom: 0; padding-left: 1.2rem; }
    .panel li { margin-bottom: 0.3rem; }
    .panel strong { color: var(--text-primary); }

    /* ================= TECH CHIPS ================= */
    .chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .chip {
        background: var(--accent-soft);
        color: var(--accent-dark);
        border: 1px solid var(--accent-soft-2);
        border-radius: 999px;
        padding: 0.4rem 0.9rem;
        font-size: 0.85rem;
        font-weight: 600;
        transition: background-color 0.15s ease, transform 0.15s ease;
    }
    .chip:hover {
        background: var(--accent-soft-2);
        transform: translateY(-1px);
    }
    .chip-group-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.6rem;
    }

    /* ================= WORKFLOW (horizontal) ================= */
    .workflow-track {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.3rem 1.5rem;
        box-shadow: var(--shadow-sm);
    }
    .workflow-step {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        background: var(--accent-soft);
        border: 1px solid var(--accent-soft-2);
        border-radius: var(--radius-sm);
        padding: 0.55rem 0.9rem;
        font-size: 0.84rem;
        font-weight: 600;
        color: var(--accent-dark);
        white-space: nowrap;
    }
    .workflow-step .step-num {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 20px; height: 20px;
        background: var(--accent);
        color: #fff;
        border-radius: 50%;
        font-size: 0.68rem;
        font-weight: 700;
    }
    .workflow-arrow {
        color: #94a3b8;
        font-size: 1rem;
        margin: 0 0.5rem;
    }

    /* ================= DIVIDER ================= */
    .thin-divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 0.5rem 0 0.5rem 0;
    }

    /* ================= SIDEBAR ================= */
    section[data-testid="stSidebar"] {
        background-color: var(--surface);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }

    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.4rem 1rem 1rem 1rem;
        margin-bottom: 0.4rem;
        border-bottom: 1px solid var(--border);
    }
    .sidebar-brand .logo {
        width: 34px; height: 34px;
        display: flex; align-items: center; justify-content: center;
        background: var(--accent);
        border-radius: var(--radius-sm);
        font-size: 1.1rem;
    }
    .sidebar-brand .name {
        font-size: 0.92rem;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1.2;
    }
    .sidebar-brand .tag {
        font-size: 0.72rem;
        color: var(--text-muted);
    }

    /* sidebar page navigation (multipage app links) */
    div[data-testid="stSidebarNav"] {
        background-color: var(--surface);
        padding-top: 0.3rem;
    }
    div[data-testid="stSidebarNav"] ul {
        padding-left: 0.6rem;
        padding-right: 0.6rem;
    }
    div[data-testid="stSidebarNav"] li {
        margin-bottom: 0.15rem;
    }
    div[data-testid="stSidebarNav"] a,
    div[data-testid="stSidebarNav"] span {
        color: var(--text-secondary) !important;
        font-size: 0.92rem;
        font-weight: 500;
        border-radius: var(--radius-sm);
    }
    div[data-testid="stSidebarNav"] a {
        padding: 0.5rem 0.7rem;
        transition: background-color 0.15s ease, color 0.15s ease;
    }
    div[data-testid="stSidebarNav"] a:hover {
        background-color: var(--accent-soft);
    }
    div[data-testid="stSidebarNav"] a:hover span {
        color: var(--accent) !important;
    }
    div[data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: var(--accent-soft);
        border-left: 3px solid var(--accent);
    }
    div[data-testid="stSidebarNav"] a[aria-current="page"] span {
        color: var(--accent-dark) !important;
        font-weight: 700;
    }
    div[data-testid="stSidebarNav"] + div {
        border-top: 1px solid var(--border);
        margin-top: 0.6rem;
        padding-top: 0.8rem;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: var(--text-primary);
    }
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] small {
        color: var(--text-muted) !important;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SIDEBAR BRAND HEADER
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="logo">🏭</div>
        <div>
            <div class="name">Factory Optimisation</div>
            <div class="tag">Analytics Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------
# HERO BANNER
# ------------------------------------------------------------------
st.markdown("""
<div class="hero-banner fade-in">
    <div class="hero-icon-badge">🏭</div>
    <div class="hero-title">Factory Optimisation System</div>
    <div class="hero-subtitle">
        An intelligent manufacturing analytics &amp; decision support platform that turns
        raw production data into forecasts, profit estimates, and optimisation recommendations.
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# PROJECT OVERVIEW
# ------------------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">📌</span> Project Overview</div>
""", unsafe_allow_html=True)
st.markdown("""
<div class="panel fade-in">
<p>
The <strong>Factory Optimisation System</strong> is a machine learning-powered web application
that helps analyze manufacturing data, forecast sales, and estimate gross profit.
It provides valuable insights that support production planning and business
decision-making through interactive dashboards and predictive analytics.
</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# PROJECT OBJECTIVES
# ------------------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">🎯</span> Project Objectives</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

objectives_left = [
    ("📈", "Forecast future sales using machine learning."),
    ("💰", "Estimate gross profit for production planning."),
    ("📊", "Analyze historical manufacturing performance."),
]
objectives_right = [
    ("🏭", "Support factory optimization decisions."),
    ("📉", "Visualize key business metrics."),
    ("🤖", "Demonstrate practical applications of AI in manufacturing."),
]

with col1:
    for icon, text in objectives_left:
        st.markdown(f"""
        <div class="info-card">
            <div class="icon-badge">{icon}</div>
            <div class="text">{text}</div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    for icon, text in objectives_right:
        st.markdown(f"""
        <div class="info-card">
            <div class="icon-badge">{icon}</div>
            <div class="text">{text}</div>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------
# KEY FEATURES
# ------------------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">✨</span> Key Features</div>
""", unsafe_allow_html=True)

features = [
    ("📊", "Interactive Dashboard"),
    ("🏭", "Factory Optimization"),
    ("🤖", "Machine Learning Models"),
    ("📈", "Sales Prediction"),
    ("📉", "Business Analytics"),
    ("📋", "Performance Insights"),
]

col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]
for i, (icon, label) in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="feature-card">
            <div class="icon-badge">{icon}</div>
            <div class="text">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------
# TECHNOLOGIES USED
# ------------------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">🛠</span> Technologies Used</div>
""", unsafe_allow_html=True)

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.markdown('<div class="chip-group-label">Core</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chip-row">
        <span class="chip">Python</span>
        <span class="chip">Streamlit</span>
        <span class="chip">Pandas</span>
        <span class="chip">NumPy</span>
    </div>
    """, unsafe_allow_html=True)

with tech2:
    st.markdown('<div class="chip-group-label">Machine Learning</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chip-row">
        <span class="chip">Scikit-learn</span>
        <span class="chip">Joblib</span>
        <span class="chip">Matplotlib</span>
        <span class="chip">Plotly</span>
    </div>
    """, unsafe_allow_html=True)

with tech3:
    st.markdown('<div class="chip-group-label">Tooling</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="chip-row">
        <span class="chip">VS Code</span>
        <span class="chip">Jupyter</span>
        <span class="chip">Git</span>
        <span class="chip">ML</span>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------
# DATASET
# ------------------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">📂</span> Dataset</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="panel">
<p>
This project is developed using the <strong>Nassau Candy Distributor Dataset</strong> containing
historical manufacturing and sales records.
</p>
<p>The dataset includes:</p>
<ul>
    <li>Order Information</li>
    <li>Product Categories</li>
    <li>Sales</li>
    <li>Manufacturing Cost</li>
    <li>Gross Profit</li>
    <li>Units Sold</li>
    <li>Regional Sales</li>
    <li>Shipping Details</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# PROJECT WORKFLOW
# ------------------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">🚀</span> Project Workflow</div>
""", unsafe_allow_html=True)

workflow_steps = [
    "Data Collection",
    "Data Cleaning",
    "EDA",
    "Feature Engineering",
    "Model Training",
    "Sales Prediction",
    "Factory Optimization",
    "Business Insights",
]

steps_html = ""
for i, step in enumerate(workflow_steps, start=1):
    steps_html += f'<div class="workflow-step"><span class="step-num">{i}</span>{step}</div>'
    if i < len(workflow_steps):
        steps_html += '<span class="workflow-arrow">→</span>'

st.markdown(f'<div class="workflow-track">{steps_html}</div>', unsafe_allow_html=True)