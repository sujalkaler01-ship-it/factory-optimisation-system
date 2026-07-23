import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from pathlib import Path

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------
st.set_page_config(
    page_title="Visualization",
    page_icon="📉",
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
        --warning: #d97706;
        --danger: #dc2626;
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
        padding: 1.1rem 1.3rem 0.4rem 1.3rem;
        box-shadow: var(--shadow-sm);
        transition: box-shadow 0.18s ease;
        margin-bottom: 1.5rem;
    }
    .chart-card:hover {
        box-shadow: var(--shadow-md);
    }

    /* ================= DATAFRAME ================= */
    .stDataFrame {
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        overflow: hidden;
    }

    /* ================= DOWNLOAD BUTTON ================= */
    div[data-testid="stDownloadButton"] > button {
        background: var(--surface);
        color: var(--accent-dark);
        border: 1.5px solid var(--accent);
        border-radius: var(--radius-sm);
        padding: 0.55rem 1.4rem;
        font-weight: 700;
        font-size: 0.92rem;
        transition: background-color 0.15s ease, transform 0.15s ease;
    }
    div[data-testid="stDownloadButton"] > button:hover {
        background: var(--accent-soft);
        transform: translateY(-1px);
        color: var(--accent-dark);
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
# HEADER
# ------------------------------------------------------------------
st.markdown('<div class="page-title fade-in">📉 Data Visualization</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Explore the manufacturing and sales data through interactive visualizations.</div>',
    unsafe_allow_html=True,
)

# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "Nassau Candy Distributor.csv"

df = pd.read_csv(DATA_PATH)

# -------------------------------------------------------
# Date Processing
# -------------------------------------------------------
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)

df["Year"] = df["Order Date"].dt.year

df["Month"] = pd.Categorical(
    df["Order Date"].dt.strftime("%b"),
    categories=[
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ],
    ordered=True
)

# NOTE: "Profit Margin (%)" isn't in the raw CSV — computing it here so the
# histogram below doesn't raise a KeyError.
df["Profit Margin (%)"] = (df["Gross Profit"] / df["Sales"]) * 100

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------
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

    st.markdown("### 🔍 Filters")

    region = st.multiselect(
        "Region",
        sorted(df["Region"].unique()),
        default=sorted(df["Region"].unique())
    )

    division = st.multiselect(
        "Division",
        sorted(df["Division"].unique()),
        default=sorted(df["Division"].unique())
    )

    year = st.multiselect(
        "Year",
        sorted(df["Year"].unique()),
        default=sorted(df["Year"].unique())
    )

    ship_mode = st.multiselect(
        "Ship Mode",
        sorted(df["Ship Mode"].unique()),
        default=sorted(df["Ship Mode"].unique())
    )

    st.markdown("---")
    st.caption("Factory Optimisation System")

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Division"].isin(division)) &
    (df["Year"].isin(year)) &
    (df["Ship Mode"].isin(ship_mode))
]

if filtered_df.empty:
    st.warning("No records match the current filters.")
    st.stop()

# ------------------------------------------------------------------
# CHART THEME HELPER
# ------------------------------------------------------------------
ACCENT = "#2563eb"
ACCENT_SCALE = ["#dbeafe", "#93c5fd", "#60a5fa", "#3b82f6", "#2563eb", "#1e40af"]


def style_fig(fig, height=380):
    """
    Applies the shared corporate look to a Plotly figure.
    IMPORTANT: does not blindly set `title_font` on every figure — doing so
    creates a phantom title object (rendered as the literal text
    "undefined") on any figure that was never given a `title=` string.
    Instead, title styling is only applied if a real title text exists.
    """
    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#334155", family="Inter, Segoe UI, sans-serif", size=12),
        margin=dict(l=10, r=10, t=45, b=10),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#ffffff", font_color="#0f172a", bordercolor="#e2e8f0"),
    )
    if fig.layout.title and fig.layout.title.text:
        fig.update_layout(title_font=dict(size=14, color="#0f172a"))
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


# -------------------------------------------------------
# Monthly Sales Trend
# -------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">📈</span> Monthly Sales Trend</div>
""", unsafe_allow_html=True)

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales",
)
fig1.update_traces(line=dict(color=ACCENT, width=2.5), marker=dict(size=7, color=ACCENT))
fig1 = style_fig(fig1)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# Monthly Gross Profit
# -------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">💰</span> Monthly Gross Profit</div>
""", unsafe_allow_html=True)

monthly_profit = (
    filtered_df.groupby("Month")["Gross Profit"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    monthly_profit,
    x="Month",
    y="Gross Profit",
    color_discrete_sequence=[ACCENT],
    title="Monthly Gross Profit",
)
fig2.update_traces(marker_line_width=0)
fig2 = style_fig(fig2)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# Top 10 Products + Sales by State
# -------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">📦</span> Products &amp; Regional Sales</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    top_products = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .nlargest(10)
        .reset_index()
        .sort_values("Sales")
    )

    fig3 = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        color="Sales",
        color_continuous_scale=ACCENT_SCALE,
        title="Top 10 Products",
    )
    fig3.update_traces(marker_line_width=0)
    fig3.update_layout(coloraxis_showscale=False)
    fig3 = style_fig(fig3, height=420)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    state_sales = (
        filtered_df.groupby("State/Province")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig4 = px.bar(
        state_sales,
        x="State/Province",
        y="Sales",
        color="Sales",
        color_continuous_scale=ACCENT_SCALE,
        title="Sales by State",
    )
    fig4.update_traces(marker_line_width=0)
    fig4.update_layout(coloraxis_showscale=False)
    fig4.update_xaxes(tickangle=-45)
    fig4 = style_fig(fig4, height=420)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# Scatter Plot + Profit Margin Distribution
# -------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">📊</span> Profitability Patterns</div>
""", unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    fig5 = px.scatter(
        filtered_df,
        x="Sales",
        y="Gross Profit",
        color="Division",
        size="Units",
        hover_data=["Region", "Product Name"],
        color_discrete_sequence=["#2563eb", "#f59e0b", "#0ea5e9", "#64748b"],
        title="Sales vs Gross Profit",
    )
    fig5 = style_fig(fig5, height=400)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    fig6 = px.histogram(
        filtered_df,
        x="Profit Margin (%)",
        nbins=30,
        color_discrete_sequence=[ACCENT],
        title="Profit Margin Distribution",
    )
    fig6.update_traces(marker_line_width=0)
    fig6 = style_fig(fig6, height=400)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# Correlation Heatmap
# -------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">🔥</span> Correlation Heatmap</div>
""", unsafe_allow_html=True)

corr = filtered_df[
    ["Sales", "Cost", "Gross Profit", "Units"]
].corr()

heatmap = ff.create_annotated_heatmap(
    z=corr.values,
    x=list(corr.columns),
    y=list(corr.index),
    annotation_text=corr.round(2).values,
    colorscale=[[0, "#eff6ff"], [0.5, "#93c5fd"], [1, "#1e40af"]],
    showscale=True,
)
heatmap.update_layout(title=dict(text="Feature Correlation", x=0.0))
heatmap = style_fig(heatmap, height=380)
heatmap.update_annotations(font=dict(color="#0f172a", size=12))

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(heatmap, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# Dataset Preview
# -------------------------------------------------------
st.markdown("""
<div class="section-header"><span class="badge-icon">📋</span> Dataset Preview</div>
""", unsafe_allow_html=True)

st.dataframe(filtered_df, use_container_width=True)

# -------------------------------------------------------
# Download Button
# -------------------------------------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Filtered Dataset",
    data=csv,
    file_name="filtered_factory_data.csv",
    mime="text/csv"
)