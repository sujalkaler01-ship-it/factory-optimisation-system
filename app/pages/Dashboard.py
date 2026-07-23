"""
Dashboard.py
Clean, corporate-themed overview / KPI page for the Nassau Candy Distributor dataset.
Drop this into your `pages/` folder (Streamlit multipage app convention).
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ------------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard | Factory Optimisation",
    page_icon="🍫",
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
        max-width: 1300px;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .fade-in { animation: fadeInUp 0.45s ease both; }

    /* ================= PAGE HEADER ================= */
    .page-title {
        font-size: 1.9rem;
        font-weight: 800;
        color: var(--text-primary);
        margin-bottom: 0.15rem;
        letter-spacing: -0.02em;
    }
    .page-subtitle {
        font-size: 0.95rem;
        color: var(--text-muted);
        margin-bottom: 1.8rem;
    }

    /* ================= KPI CARDS ================= */
    .kpi-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-top: 3px solid var(--accent);
        border-radius: var(--radius-md);
        padding: 1.1rem 1.3rem;
        box-shadow: var(--shadow-sm);
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-hover);
    }
    .kpi-label {
        font-size: 0.76rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.1;
    }
    .kpi-delta-pos {
        font-size: 0.8rem;
        color: var(--success);
        margin-top: 0.4rem;
        font-weight: 600;
    }
    .kpi-delta-neg {
        font-size: 0.8rem;
        color: var(--danger);
        margin-top: 0.4rem;
        font-weight: 600;
    }

    /* ================= SECTION HEADERS ================= */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 2rem 0 0.9rem 0;
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

    /* ================= CHART CARDS ================= */
    .chart-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.1rem 1.3rem 0.5rem 1.3rem;
        box-shadow: var(--shadow-sm);
        transition: box-shadow 0.18s ease;
    }
    .chart-card:hover {
        box-shadow: var(--shadow-md);
    }
    .chart-card-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: var(--text-secondary);
        margin-bottom: 0.3rem;
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

    /* ================= DATAFRAME ================= */
    .stDataFrame {
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------
# DATA LOADING
# ------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    candidates = [
        Path("data/Nassau Candy Distributor.csv"),
        Path("data/Nassau_Candy_Distributor.csv"),
        Path("../data/Nassau Candy Distributor.csv"),
    ]
    path = next((p for p in candidates if p.exists()), None)
    if path is None:
        st.error(
            "Could not find the dataset. Expected it at `data/Nassau Candy Distributor.csv`. "
            "Update the path in `load_data()` if your file lives elsewhere."
        )
        st.stop()

    df = pd.read_csv(path)
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y")
    df["Profit Margin"] = (df["Gross Profit"] / df["Sales"]) * 100
    df["Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    return df


df = load_data()

# ------------------------------------------------------------------
# SIDEBAR
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

    st.markdown("### Filters")

    date_min, date_max = df["Order Date"].min(), df["Order Date"].max()
    date_range = st.date_input(
        "Order date range",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
    )

    divisions = st.multiselect(
        "Division", options=sorted(df["Division"].unique()), default=None,
        placeholder="All divisions",
    )
    regions = st.multiselect(
        "Region", options=sorted(df["Region"].unique()), default=None,
        placeholder="All regions",
    )
    ship_modes = st.multiselect(
        "Ship mode", options=sorted(df["Ship Mode"].unique()), default=None,
        placeholder="All ship modes",
    )

    st.markdown("---")
    st.caption("Factory Optimisation System")

# apply filters
mask = pd.Series(True, index=df.index)
if len(date_range) == 2:
    mask &= (df["Order Date"] >= pd.Timestamp(date_range[0])) & (
        df["Order Date"] <= pd.Timestamp(date_range[1])
    )
if divisions:
    mask &= df["Division"].isin(divisions)
if regions:
    mask &= df["Region"].isin(regions)
if ship_modes:
    mask &= df["Ship Mode"].isin(ship_modes)

fdf = df[mask]

if fdf.empty:
    st.warning("No records match the current filters.")
    st.stop()

# ------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------
st.markdown('<div class="page-title fade-in">Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Overview of sales, profit, and order activity</div>',
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# KPI ROW
# ------------------------------------------------------------------
total_sales = fdf["Sales"].sum()
total_profit = fdf["Gross Profit"].sum()
total_units = fdf["Units"].sum()
avg_margin = (total_profit / total_sales * 100) if total_sales else 0
total_orders = fdf["Order ID"].nunique()

kpis = [
    ("Total Sales", f"${total_sales:,.0f}"),
    ("Gross Profit", f"${total_profit:,.0f}"),
    ("Avg. Margin", f"{avg_margin:.1f}%"),
    ("Total Orders", f"{total_orders:,}"),
    ("Units Sold", f"{total_units:,}"),
]

cols = st.columns(len(kpis))
for col, (label, value) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------
# CHART THEME HELPER
# ------------------------------------------------------------------
def style_fig(fig, height=340):
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#334155", family="Inter, Segoe UI, sans-serif", size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.2),
        hoverlabel=dict(bgcolor="#ffffff", font_color="#0f172a", bordercolor="#e2e8f0"),
    )
    fig.update_xaxes(
        showgrid=False, zeroline=False, linecolor="#e2e8f0",
        tickfont=dict(color="#0f172a", size=12),
        title_font=dict(color="#0f172a", size=13),
    )
    fig.update_yaxes(
        showgrid=True, gridcolor="#eef2f7", zeroline=False,
        tickfont=dict(color="#0f172a", size=12),
        title_font=dict(color="#0f172a", size=13),
    )
    return fig


ACCENT = "#2563eb"
ACCENT_SOFT = ["#2563eb", "#60a5fa", "#93c5fd", "#1e40af", "#0ea5e9"]

# ------------------------------------------------------------------
# ROW: Sales trend + Division split
# ------------------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">📈</span> Sales Trend &amp; Mix</div>
""", unsafe_allow_html=True)
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown('<div class="chart-card"><div class="chart-card-title">Monthly Sales vs Gross Profit</div>', unsafe_allow_html=True)
    monthly = fdf.groupby("Month", as_index=False)[["Sales", "Gross Profit"]].sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Sales"], name="Sales",
        line=dict(color=ACCENT, width=2.5), fill="tozeroy",
        fillcolor="rgba(37,99,235,0.08)",
    ))
    fig.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Gross Profit"], name="Gross Profit",
        line=dict(color="#0ea5e9", width=2.5, dash="dot"),
    ))
    fig = style_fig(fig)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-card"><div class="chart-card-title">Sales by Division</div>', unsafe_allow_html=True)
    div_sales = fdf.groupby("Division", as_index=False)["Sales"].sum()
    fig = px.pie(
        div_sales, names="Division", values="Sales", hole=0.62,
        color_discrete_sequence=ACCENT_SOFT,
    )
    fig.update_traces(textinfo="percent+label", textfont_size=11)
    fig = style_fig(fig)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------
# ROW: Region performance + Ship mode
# ------------------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">🌎</span> Regional &amp; Fulfilment Breakdown</div>
""", unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="chart-card"><div class="chart-card-title">Sales by Region</div>', unsafe_allow_html=True)
    region_sales = fdf.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales")
    fig = px.bar(
        region_sales, x="Sales", y="Region", orientation="h",
        color_discrete_sequence=[ACCENT],
    )
    fig.update_traces(marker_line_width=0)
    fig = style_fig(fig)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="chart-card"><div class="chart-card-title">Orders by Ship Mode</div>', unsafe_allow_html=True)
    ship_counts = fdf["Ship Mode"].value_counts().reset_index()
    ship_counts.columns = ["Ship Mode", "Orders"]
    fig = px.bar(
        ship_counts, x="Ship Mode", y="Orders",
        color_discrete_sequence=[ACCENT],
    )
    fig.update_traces(marker_line_width=0)
    fig = style_fig(fig)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------
# TOP PRODUCTS TABLE
# ------------------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">🏆</span> Top Products by Sales</div>
""", unsafe_allow_html=True)

top_products = (
    fdf.groupby("Product Name", as_index=False)
    .agg(Sales=("Sales", "sum"), Units=("Units", "sum"), Gross_Profit=("Gross Profit", "sum"))
    .sort_values("Sales", ascending=False)
    .head(10)
)
top_products["Margin %"] = (top_products["Gross_Profit"] / top_products["Sales"] * 100).round(1)
top_products = top_products.rename(columns={"Gross_Profit": "Gross Profit"})

st.dataframe(
    top_products.style.format({
        "Sales": "${:,.2f}",
        "Gross Profit": "${:,.2f}",
        "Margin %": "{:.1f}%",
    }),
    use_container_width=True,
    hide_index=True,
)