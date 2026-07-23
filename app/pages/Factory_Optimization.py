import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Factory Optimization",
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
        --success-soft: #f0fdf4;
        --warning: #d97706;
        --warning-soft: #fffbeb;
        --danger: #dc2626;
        --danger-soft: #fef2f2;
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.05);
        --shadow-md: 0 4px 16px rgba(15, 23, 42, 0.06);
        --shadow-hover: 0 8px 24px rgba(37, 99, 235, 0.10);
    }

    /* ================= BASE ================= */
    .stApp { background: var(--bg); }
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

    /* ================= HERO STRIP ================= */
    .page-hero {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.8rem;
    }
    .page-hero .hero-icon {
        width: 52px; height: 52px;
        flex-shrink: 0;
        display: flex; align-items: center; justify-content: center;
        background: var(--accent-soft);
        border: 1px solid var(--accent-soft-2);
        border-radius: var(--radius-md);
        font-size: 1.7rem;
    }
    .page-title {
        font-size: 1.9rem;
        font-weight: 800;
        color: var(--text-primary);
        margin-bottom: 0.1rem;
        letter-spacing: -0.02em;
    }
    .page-subtitle {
        font-size: 0.95rem;
        color: var(--text-muted);
    }

    /* ================= SECTION HEADERS ================= */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 1.8rem 0 0.9rem 0;
    }
    .section-header .badge-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px; height: 28px;
        background: var(--accent-soft);
        border-radius: var(--radius-sm);
        font-size: 0.9rem;
    }

    /* ================= FORM PANEL ================= */
    .form-panel {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.6rem 1.8rem 0.6rem 1.8rem;
        box-shadow: var(--shadow-sm);
        margin-bottom: 1.2rem;
    }
    .form-panel-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.8rem;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid var(--border-soft);
    }

    /* ================= STREAMLIT WIDGET RESKIN ================= */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stNumberInput"] label {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-secondary);
    }
    div[data-baseweb="select"] > div,
    div[data-testid="stNumberInput"] input {
        border-radius: var(--radius-sm) !important;
        border-color: var(--border) !important;
    }
    div[data-baseweb="select"] > div:focus-within,
    div[data-testid="stNumberInput"] input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.12) !important;
    }

    /* primary button */
    div.stButton > button {
        background: var(--accent);
        color: #ffffff;
        border: none;
        border-radius: var(--radius-sm);
        padding: 0.65rem 1.8rem;
        font-weight: 700;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: background-color 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
    }
    div.stButton > button:hover {
        background: var(--accent-dark);
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(30, 64, 175, 0.3);
        color: #ffffff;
    }
    div.stButton > button:active {
        transform: translateY(0);
    }

    /* ================= RESULT KPI CARDS ================= */
    .result-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.1rem 1.3rem;
        box-shadow: var(--shadow-sm);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        display: flex;
        align-items: center;
        gap: 0.9rem;
    }
    .result-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-hover);
    }
    .result-card .icon-badge {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 42px; height: 42px;
        background: var(--accent-soft);
        border-radius: var(--radius-sm);
        font-size: 1.15rem;
    }
    .result-label {
        font-size: 0.76rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }
    .result-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.1;
    }

    /* ================= INSIGHT BANNERS ================= */
    .insight-banner {
        border-radius: var(--radius-md);
        padding: 1rem 1.2rem;
        font-size: 0.92rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-top: 1.1rem;
        box-shadow: var(--shadow-sm);
    }
    .insight-success {
        background: var(--success-soft);
        border: 1px solid #bbf7d0;
        color: #15803d;
    }
    .insight-info {
        background: var(--accent-soft);
        border: 1px solid var(--accent-soft-2);
        color: var(--accent-dark);
    }
    .insight-warning {
        background: var(--warning-soft);
        border: 1px solid #fde68a;
        color: #b45309;
    }

    /* ================= SIDEBAR ================= */
    section[data-testid="stSidebar"] {
        background-color: var(--surface);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] > div { padding-top: 1rem; }

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

    div[data-testid="stSidebarNav"] { background-color: var(--surface); padding-top: 0.3rem; }
    div[data-testid="stSidebarNav"] ul { padding-left: 0.6rem; padding-right: 0.6rem; }
    div[data-testid="stSidebarNav"] li { margin-bottom: 0.15rem; }
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
    div[data-testid="stSidebarNav"] a:hover { background-color: var(--accent-soft); }
    div[data-testid="stSidebarNav"] a:hover span { color: var(--accent) !important; }
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
    section[data-testid="stSidebar"] p { color: var(--text-primary); }
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] small { color: var(--text-muted) !important; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SIDEBAR BRAND
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
# HEADER
# ------------------------------------------------------------------
st.markdown("""
<div class="page-hero fade-in">
    <div class="hero-icon">🏭</div>
    <div>
        <div class="page-title">Factory Optimization</div>
        <div class="page-subtitle">Estimate expected <strong>Gross Profit</strong> using the trained Random Forest model.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Load Model
# ---------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "random_forest_profit.pkl"

model = joblib.load(MODEL_PATH)

# ---------------------------------------------------
# User Inputs
# ---------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">⚙️</span> Production Parameters</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-panel">', unsafe_allow_html=True)
st.markdown('<div class="form-panel-label">Enter production details below</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    division = st.selectbox(
        "Division",
        ["Chocolate", "Other", "Sugar"]
    )

    region = st.selectbox(
        "Region",
        ["Atlantic", "Gulf", "Interior", "Pacific"]
    )

    units = st.number_input(
        "Units",
        min_value=1,
        value=10
    )

with col2:
    sales = st.number_input(
        "Sales ($)",
        min_value=0.0,
        value=100.0,
        step=1.0
    )

    cost = st.number_input(
        "Cost ($)",
        min_value=0.0,
        value=60.0,
        step=1.0
    )

st.markdown("</div>", unsafe_allow_html=True)

optimize_clicked = st.button("🏭 Optimize Factory")

# ---------------------------------------------------
# Prediction
# ---------------------------------------------------
if optimize_clicked:

    division_map = {
        "Chocolate": 0,
        "Other": 1,
        "Sugar": 2
    }

    region_map = {
        "Atlantic": 0,
        "Gulf": 1,
        "Interior": 2,
        "Pacific": 3
    }

    input_data = pd.DataFrame({
        "Division": [division_map[division]],
        "Region": [region_map[region]],
        "Units": [units],
        "Sales": [sales],
        "Cost": [cost]
    })

    prediction = model.predict(input_data)[0]
    profit_margin = (prediction / sales) * 100 if sales > 0 else 0

    # -----------------------------
    # Result KPI cards
    # -----------------------------
    st.markdown("""
    <div class="section-header"><span class="badge-icon">📊</span> Business Insights</div>
    """, unsafe_allow_html=True)

    rcol1, rcol2 = st.columns(2)

    with rcol1:
        st.markdown(f"""
        <div class="result-card fade-in">
            <div class="icon-badge">💰</div>
            <div>
                <div class="result-label">Estimated Gross Profit</div>
                <div class="result-value">${prediction:,.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with rcol2:
        st.markdown(f"""
        <div class="result-card fade-in">
            <div class="icon-badge">📈</div>
            <div>
                <div class="result-label">Estimated Profit Margin</div>
                <div class="result-value">{profit_margin:.2f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # -----------------------------
    # Insight banner based on margin
    # -----------------------------
    if profit_margin >= 40:
        st.markdown("""
        <div class="insight-banner insight-success">
            ✅ Excellent profit margin. This production plan looks highly profitable.
        </div>
        """, unsafe_allow_html=True)

    elif profit_margin >= 25:
        st.markdown("""
        <div class="insight-banner insight-info">
            ℹ️ Moderate profit margin. Production appears financially healthy.
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="insight-banner insight-warning">
            ⚠️ Low profit margin. Consider reducing costs or increasing sales price.
        </div>
        """, unsafe_allow_html=True)