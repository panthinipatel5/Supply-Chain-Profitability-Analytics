"""
APL Logistics — Customer, Product & Profitability Performance Dashboard
Fintech-styled Streamlit application (white base, light-to-dark blue accents).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="APL Logistics | Profitability Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# DESIGN TOKENS
# ---------------------------------------------------------------------------
NAVY = "#0A2540"
BLUE_DEEP = "#0B3D91"
BLUE_PRIMARY = "#1D5FBF"
BLUE_MID = "#3E8DED"
BLUE_LIGHT = "#7FB6F7"
BLUE_PALE = "#DCEAFB"
BG_PAGE = "#F5F8FC"
BORDER = "#E3EAF3"
MUTED = "#5B7089"
NEGATIVE = "#D64545"
POSITIVE = "#1D5FBF"

SEQ_BLUES = [NAVY, BLUE_DEEP, BLUE_PRIMARY, BLUE_MID, BLUE_LIGHT, BLUE_PALE]
DIVERGING = ["#D64545", "#F3B8B8", BLUE_PALE, BLUE_LIGHT, BLUE_PRIMARY, BLUE_DEEP]

PLOTLY_LAYOUT = dict(
    font=dict(family="'Inter', 'Segoe UI', sans-serif", color=NAVY, size=13),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    title_font=dict(size=16, color=NAVY),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
    margin=dict(t=60, l=10, r=10, b=10),
)

# ---------------------------------------------------------------------------
# GLOBAL CSS — fintech identity
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', 'Segoe UI', sans-serif;
}}

.stApp {{
    background: {BG_PAGE};
}}

section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {NAVY} 0%, {BLUE_DEEP} 100%);
    border-right: 1px solid {BORDER};
}}
section[data-testid="stSidebar"] * {{
    color: #EAF2FB !important;
}}
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {{
    background-color: {BLUE_PRIMARY} !important;
}}
section[data-testid="stSidebar"] hr {{
    border-color: rgba(255,255,255,0.15);
}}

/* Header band */
.hero-band {{
    background: linear-gradient(120deg, {NAVY} 0%, {BLUE_DEEP} 55%, {BLUE_PRIMARY} 100%);
    padding: 28px 36px;
    border-radius: 16px;
    margin-bottom: 22px;
    box-shadow: 0 8px 24px rgba(10, 37, 64, 0.18);
}}
.hero-eyebrow {{
    color: {BLUE_LIGHT};
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
}}
.hero-title {{
    color: #FFFFFF;
    font-size: 30px;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.5px;
}}
.hero-sub {{
    color: #C9DCF5;
    font-size: 14px;
    margin-top: 6px;
    font-weight: 400;
}}

/* KPI cards */
.kpi-card {{
    background: #FFFFFF;
    border: 1px solid {BORDER};
    border-top: 3px solid {BLUE_PRIMARY};
    border-radius: 12px;
    padding: 16px 18px;
    box-shadow: 0 2px 10px rgba(10, 37, 64, 0.05);
    height: 100%;
}}
.kpi-label {{
    color: {MUTED};
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
}}
.kpi-value {{
    color: {NAVY};
    font-size: 24px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: -0.5px;
}}
.kpi-delta-pos {{ color: {BLUE_PRIMARY}; font-size: 12px; font-weight: 600; margin-top: 4px; }}
.kpi-delta-neg {{ color: {NEGATIVE}; font-size: 12px; font-weight: 600; margin-top: 4px; }}

/* Section headers */
.section-title {{
    color: {NAVY};
    font-size: 19px;
    font-weight: 700;
    margin: 8px 0 2px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid {BLUE_PALE};
}}
.section-caption {{
    color: {MUTED};
    font-size: 13px;
    margin-bottom: 14px;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    gap: 6px;
    border-bottom: 1px solid {BORDER};
}}
.stTabs [data-baseweb="tab"] {{
    background-color: transparent;
    border-radius: 8px 8px 0 0;
    padding: 10px 18px;
    color: {MUTED};
    font-weight: 600;
    font-size: 14px;
}}
.stTabs [aria-selected="true"] {{
    background-color: {BLUE_PALE} !important;
    color: {NAVY} !important;
}}

/* Dataframe container */
[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER};
    border-radius: 10px;
    overflow: hidden;
}}

/* Metric-ish badge pill */
.pill {{
    display: inline-block;
    background: {BLUE_PALE};
    color: {BLUE_DEEP};
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.5px;
}}
.pill-neg {{
    background: #FBE4E4;
    color: {NEGATIVE};
}}

footer {{visibility: hidden;}}
#MainMenu {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ============================================================
   READABILITY FIX — Streamlit text only
   Keep the original dashboard UI and do not override Plotly.
   ============================================================ */

.stApp p,
.stApp label,
.stApp li,
.stApp td,
.stApp th {
    color: #172033;
}

.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6 {
    color: #0A2540 !important;
}

/* Preserve original dark sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A2540 0%, #0B3D91 100%) !important;
}

section[data-testid="stSidebar"] * {
    color: #EAF2FB !important;
}

/* Inputs */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF;
}

div[data-baseweb="select"] *,
div[data-baseweb="input"] *,
div[data-baseweb="textarea"] * {
    color: #172033 !important;
}

/* KPI cards */
div[data-testid="stMetric"] {
    background: #FFFFFF;
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
    color: #526071 !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: #0A2540 !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #526071 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #0B3D91 !important;
}

/* Tables */
[data-testid="stDataFrame"] *,
[data-testid="stTable"] * {
    color: #172033 !important;
}

/* Expanders */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
    color: #172033 !important;
}

/* Buttons */
.stButton > button {
    color: #FFFFFF !important;
}

.stCaption,
small {
    color: #526071 !important;
}

.stApp a {
    color: #0B3D91 !important;
}

/* Plotly chart text: explicitly keep axes, labels and legends dark */
.js-plotly-plot .xtick text,
.js-plotly-plot .ytick text,
.js-plotly-plot .axis-title,
.js-plotly-plot .g-xtitle text,
.js-plotly-plot .g-ytitle text,
.js-plotly-plot .legendtext,
.js-plotly-plot .annotation-text,
.js-plotly-plot .colorbar .tick text,
.js-plotly-plot .g-gtitle text {
    fill: #0A2540 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner="Loading order data...")
def load_data():
    # Resolve paths from the dashboard file itself, not from the
    # terminal's current working directory. This keeps the dashboard
    # working even when Streamlit is launched from another folder.
    here = Path(__file__).resolve().parent
    project_root = here.parent

    # Preferred cleaned files produced by the notebook, followed by the
    # original dataset as a fallback.
    candidates = [
        project_root / "data" / "apl_clean.parquet",
        project_root / "data" / "apl_clean.csv",
        here / "data" / "apl_clean.parquet",
        here / "data" / "apl_clean.csv",
        project_root / "data" / "APL_Logistics.csv",
        here / "data" / "APL_Logistics.csv",
        Path.cwd() / "data" / "apl_clean.parquet",
        Path.cwd() / "data" / "apl_clean.csv",
        Path.cwd() / "data" / "APL_Logistics.csv",
    ]

    # Remove duplicates while preserving order.
    candidates = list(dict.fromkeys(candidates))

    data_path = next((p for p in candidates if p.is_file()), None)

    # If the normal locations are not used, search the project folder
    # for the expected files. This handles small differences in folder
    # organization without changing any dashboard UI or logic.
    if data_path is None and project_root.exists():
        filenames = {"apl_clean.parquet", "apl_clean.csv", "APL_Logistics.csv"}
        for p in project_root.rglob("*"):
            if p.is_file() and p.name in filenames:
                data_path = p
                break

    if data_path is None:
        searched = "\n".join(f"- {p}" for p in candidates)
        raise FileNotFoundError(
            "Could not locate the dataset.\n\n"
            "Place apl_clean.parquet, apl_clean.csv, or APL_Logistics.csv "
            "inside the Project_2/data folder.\n\n"
            f"Locations checked:\n{searched}"
        )

    if data_path.suffix.lower() == ".parquet":
        df = pd.read_parquet(data_path)
    else:
        df = pd.read_csv(data_path, encoding="latin1")

    if "Profit Margin %" not in df.columns:
        df["Profit Margin %"] = np.where(
            df["Sales"] != 0,
            df["Benefit per order"] / df["Sales"] * 100,
            0,
        )

    return df

df = load_data()

# ---------------------------------------------------------------------------
# SIDEBAR — FILTERS
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ◈ APL Logistics")
    st.caption("Profitability Intelligence Console")
    st.markdown("---")

    segments = sorted(df["Customer Segment"].unique().tolist())
    sel_segments = st.multiselect("Customer Segment", segments, default=segments)

    markets = sorted(df["Market"].unique().tolist())
    sel_markets = st.multiselect("Market", markets, default=markets)

    regions = sorted(df["Order Region"].unique().tolist())
    sel_regions = st.multiselect("Order Region", regions, default=regions)

    categories = sorted(df["Category Name"].unique().tolist())
    sel_categories = st.multiselect("Category", categories, default=[])
    if not sel_categories:
        sel_categories = categories

    disc_min, disc_max = float(df["Order Item Discount Rate"].min()), float(df["Order Item Discount Rate"].max())
    sel_disc = st.slider("Discount Rate Range", min_value=0.0, max_value=round(disc_max, 2),
                          value=(0.0, round(disc_max, 2)), step=0.01, format="%.2f")

    st.markdown("---")
    st.caption("Data source: APL_Logistics order-item dataset")
    st.caption(f"{len(df):,} clean order-item rows loaded")

# ---------------------------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------------------------
fdf = df[
    df["Customer Segment"].isin(sel_segments) &
    df["Market"].isin(sel_markets) &
    df["Order Region"].isin(sel_regions) &
    df["Category Name"].isin(sel_categories) &
    df["Order Item Discount Rate"].between(sel_disc[0], sel_disc[1])
]

if fdf.empty:
    st.warning("No data matches the current filters. Adjust the filters in the sidebar.")
    st.stop()

# ---------------------------------------------------------------------------
# HERO / HEADER
# ---------------------------------------------------------------------------
st.markdown(f"""
<div class="hero-band">
    <div class="hero-eyebrow">Supply Chain · Commercial Intelligence</div>
    <div class="hero-title">Customer, Product & Profitability Performance</div>
    <div class="hero-sub">Where sales are strong but margins are silently eroding — and where they aren't.</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# KPI STRIP
# ---------------------------------------------------------------------------
total_revenue = fdf["Sales"].sum()
total_profit = fdf["Benefit per order"].sum()
margin_pct = (total_profit / total_revenue * 100) if total_revenue else 0
n_customers = fdf["Customer Id"].nunique()
n_orders = fdf["Order Item Total"].count()
avg_order_value = fdf["Sales per customer"].mean()
late_risk = fdf["Late_delivery_risk"].mean() * 100

k1, k2, k3, k4, k5, k6 = st.columns(6)
kpis = [
    (k1, "Total Revenue", f"${total_revenue:,.0f}"),
    (k2, "Total Profit", f"${total_profit:,.0f}"),
    (k3, "Profit Margin", f"{margin_pct:.2f}%"),
    (k4, "Active Customers", f"{n_customers:,}"),
    (k5, "Order Items", f"{n_orders:,}"),
    (k6, "Late Delivery Risk", f"{late_risk:.1f}%"),
]
for col, label, value in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------------------------------
# TABS — DASHBOARD MODULES
# ---------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Revenue & Profit Overview",
    "👥  Customer Value",
    "📦  Product & Category",
    "🏷️  Discount Impact Analyzer",
])

# =============================================================================
# TAB 1 — REVENUE & PROFIT OVERVIEW
# =============================================================================
with tab1:
    st.markdown('<div class="section-title">Revenue vs. Profit, by Shipping Mode</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Where volume is heaviest, and whether that volume converts into profit.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.3, 1])
    with c1:
        ship = fdf.groupby("Shipping Mode").agg(Revenue=("Sales", "sum"), Profit=("Benefit per order", "sum")).reset_index()
        ship["Margin %"] = ship["Profit"] / ship["Revenue"] * 100
        ship = ship.sort_values("Revenue", ascending=False)

        fig = go.Figure()
        fig.add_bar(x=ship["Shipping Mode"], y=ship["Revenue"], name="Revenue", marker_color=BLUE_PALE)
        fig.add_bar(x=ship["Shipping Mode"], y=ship["Profit"], name="Profit", marker_color=BLUE_PRIMARY)
        fig.update_layout(barmode="group", height=380, **PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.bar(ship.sort_values("Margin %"), x="Margin %", y="Shipping Mode", orientation="h",
                      color="Margin %", color_continuous_scale=DIVERGING, title="Margin % by Shipping Mode")
        fig.update_layout(height=380, coloraxis_showscale=False, **PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Profit Concentration (Pareto)</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">What share of total profit comes from the top share of customers.</div>', unsafe_allow_html=True)

    cust_profit = fdf.groupby("Customer Id")["Benefit per order"].sum().sort_values(ascending=False).reset_index()
    cust_profit["cum_share"] = cust_profit["Benefit per order"].cumsum() / cust_profit["Benefit per order"].sum() * 100
    cust_profit["cust_share"] = np.arange(1, len(cust_profit) + 1) / len(cust_profit) * 100

    top10_cut = max(1, int(len(cust_profit) * 0.10))
    top10_share = cust_profit.iloc[:top10_cut]["Benefit per order"].sum() / max(total_profit, 1e-9) * 100

    c1, c2 = st.columns([2, 1])
    with c1:
        fig = px.area(cust_profit, x="cust_share", y="cum_share",
                       labels={"cust_share": "% of Customers", "cum_share": "Cumulative % of Profit"})
        fig.update_traces(line_color=BLUE_DEEP, fillcolor="rgba(29,95,191,0.15)")
        fig.add_shape(type="line", x0=0, y0=0, x1=100, y1=100, line=dict(dash="dot", color=MUTED))
        fig.update_layout(height=340, **PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card" style="margin-top: 40px;">
            <div class="kpi-label">Top 10% of Customers Generate</div>
            <div class="kpi-value" style="font-size: 36px;">{top10_share:.1f}%</div>
            <div class="section-caption" style="margin-top:8px;">of total profit in the current filter selection — concentration risk if these accounts churn.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Revenue by Market — Margin Overlay</div>', unsafe_allow_html=True)
    market_perf = fdf.groupby("Market").agg(Revenue=("Sales", "sum"), Profit=("Benefit per order", "sum")).reset_index()
    market_perf["Margin %"] = market_perf["Profit"] / market_perf["Revenue"] * 100
    market_perf = market_perf.sort_values("Revenue", ascending=False)

    fig = go.Figure()
    fig.add_bar(x=market_perf["Market"], y=market_perf["Revenue"], name="Revenue", marker_color=BLUE_LIGHT)
    fig.add_trace(go.Scatter(x=market_perf["Market"], y=market_perf["Margin %"], name="Margin %",
                              yaxis="y2", mode="lines+markers", line=dict(color=NAVY, width=3),
                              marker=dict(size=9)))
    fig.update_layout(
        height=400,
        yaxis=dict(title="Revenue ($)"),
        yaxis2=dict(title="Margin %", overlaying="y", side="right", showgrid=False),
        **PLOTLY_LAYOUT
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TAB 2 — CUSTOMER VALUE
# =============================================================================
with tab2:
    st.markdown('<div class="section-title">Top & Bottom Customers by Profit</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">High-value accounts to protect versus low-margin accounts to review.</div>', unsafe_allow_html=True)

    cust_perf = fdf.groupby("Customer Id").agg(
        Revenue=("Sales", "sum"), Profit=("Benefit per order", "sum"),
        Orders=("Order Item Total", "count"), Segment=("Customer Segment", "first"),
        City=("Customer City", "first"), Country=("Customer Country", "first"),
    ).reset_index()
    cust_perf["Margin %"] = cust_perf["Profit"] / cust_perf["Revenue"] * 100

    n_show = st.slider("Number of customers to show", 5, 25, 10, key="cust_n")

    c1, c2 = st.columns(2)
    with c1:
        top_c = cust_perf.sort_values("Profit", ascending=False).head(n_show)
        fig = px.bar(top_c.sort_values("Profit"), x="Profit", y="Customer Id", orientation="h",
                      title=f"Top {n_show} Customers by Profit", color_discrete_sequence=[BLUE_PRIMARY])
        fig.update_layout(height=420, yaxis_type="category", **PLOTLY_LAYOUT)
        fig.update_yaxes(tickmode="linear")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        bottom_c = cust_perf.sort_values("Profit", ascending=True).head(n_show)
        fig = px.bar(bottom_c.sort_values("Profit", ascending=False), x="Profit", y="Customer Id", orientation="h",
                      title=f"Bottom {n_show} Customers by Profit", color_discrete_sequence=[NEGATIVE])
        fig.update_layout(height=420, yaxis_type="category", **PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Customer Value Tiers</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Customers segmented into quartiles by total profit contribution.</div>', unsafe_allow_html=True)

    cust_perf["Value Tier"] = pd.qcut(cust_perf["Profit"].rank(method="first"), 4,
                                       labels=["Bronze", "Silver", "Gold", "Platinum"])
    tier_summary = cust_perf.groupby("Value Tier", observed=True).agg(
        Customers=("Customer Id", "count"), Revenue=("Revenue", "sum"), Profit=("Profit", "sum")
    ).reset_index()
    tier_summary["Avg Margin %"] = tier_summary["Profit"] / tier_summary["Revenue"] * 100

    c1, c2 = st.columns([1.3, 1])
    with c1:
        fig = px.bar(tier_summary, x="Value Tier", y="Profit", color="Value Tier",
                      color_discrete_sequence=[BLUE_PALE, BLUE_LIGHT, BLUE_PRIMARY, NAVY],
                      title="Profit Contribution by Value Tier")
        fig.update_layout(height=380, showlegend=False, **PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        seg_perf = fdf.groupby("Customer Segment").agg(Revenue=("Sales", "sum")).reset_index()
        fig = px.pie(seg_perf, names="Customer Segment", values="Revenue", hole=0.6,
                      color_discrete_sequence=[NAVY, BLUE_PRIMARY, BLUE_LIGHT],
                      title="Revenue Share by Segment")
        fig.update_layout(height=380, **PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Customer Detail Table</div>', unsafe_allow_html=True)
    st.dataframe(
        cust_perf.sort_values("Profit", ascending=False)[
            ["Customer Id", "Segment", "City", "Country", "Orders", "Revenue", "Profit", "Margin %", "Value Tier"]
        ].style.format({"Revenue": "${:,.0f}", "Profit": "${:,.0f}", "Margin %": "{:.1f}%"}),
        use_container_width=True, height=320
    )

# =============================================================================
# TAB 3 — PRODUCT & CATEGORY PERFORMANCE
# =============================================================================
with tab3:
    st.markdown('<div class="section-title">Category Profitability</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Revenue sized, margin colored — spot high-revenue, low-margin categories fast.</div>', unsafe_allow_html=True)

    cat_perf = fdf.groupby("Category Name").agg(
        Revenue=("Sales", "sum"), Profit=("Benefit per order", "sum"), Orders=("Order Item Total", "count")
    ).reset_index()
    cat_perf["Margin %"] = cat_perf["Profit"] / cat_perf["Revenue"] * 100
    cat_perf = cat_perf.sort_values("Revenue", ascending=False)

    fig = px.bar(cat_perf, x="Revenue", y="Category Name", orientation="h", color="Margin %",
                  color_continuous_scale=DIVERGING, title="Category Revenue, Colored by Margin %")
    fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=520, **PLOTLY_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-title">Product Positioning Map</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Revenue vs. margin — bubble size shows order volume. Products below the line are loss-making.</div>', unsafe_allow_html=True)

    prod_perf = fdf.groupby("Product Name").agg(
        Revenue=("Sales", "sum"), Profit=("Benefit per order", "sum"), Orders=("Order Item Total", "count")
    ).reset_index()
    prod_perf["Margin %"] = prod_perf["Profit"] / prod_perf["Revenue"] * 100

    fig = px.scatter(prod_perf, x="Revenue", y="Margin %", size="Orders", color="Margin %",
                      color_continuous_scale=DIVERGING, hover_name="Product Name", size_max=42)
    fig.add_hline(y=0, line_dash="dot", line_color=MUTED)
    fig.update_layout(height=460, **PLOTLY_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**High-revenue, low-margin products (watch list)**")
        rev_q75 = prod_perf["Revenue"].quantile(0.75)
        margin_q25 = prod_perf["Margin %"].quantile(0.25)
        watch = prod_perf[(prod_perf["Revenue"] >= rev_q75) & (prod_perf["Margin %"] <= margin_q25)]
        st.dataframe(
            watch.sort_values("Revenue", ascending=False)[["Product Name", "Revenue", "Profit", "Margin %"]]
                .style.format({"Revenue": "${:,.0f}", "Profit": "${:,.0f}", "Margin %": "{:.1f}%"}),
            use_container_width=True, height=260
        )
    with c2:
        st.markdown("**Category × Segment margin heatmap**")
        heat = fdf.groupby(["Category Name", "Customer Segment"])["Profit Margin %"].mean().reset_index()
        heat_p = heat.pivot(index="Category Name", columns="Customer Segment", values="Profit Margin %")
        fig = px.imshow(heat_p, color_continuous_scale=DIVERGING, aspect="auto",
                          labels=dict(color="Avg Margin %"))
        fig.update_layout(height=420, **PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# TAB 4 — DISCOUNT IMPACT ANALYZER
# =============================================================================
with tab4:
    st.markdown('<div class="section-title">Discount Rate vs. Margin Erosion</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">How profit margin changes as discount rates increase.</div>', unsafe_allow_html=True)

    fdf = fdf.copy()
    fdf["Discount Bucket"] = pd.cut(
        fdf["Order Item Discount Rate"],
        bins=[-0.001, 0.0, 0.05, 0.10, 0.15, 0.20, 1.0],
        labels=["0%", "0-5%", "5-10%", "10-15%", "15-20%", "20%+"]
    )
    disc_perf = fdf.groupby("Discount Bucket", observed=True).agg(
        Orders=("Order Item Total", "count"), Revenue=("Sales", "sum"), Profit=("Benefit per order", "sum")
    ).reset_index()
    disc_perf["Margin %"] = disc_perf["Profit"] / disc_perf["Revenue"] * 100

    c1, c2 = st.columns([1.3, 1])
    with c1:
        fig = px.bar(disc_perf, x="Discount Bucket", y="Margin %", color="Margin %",
                      color_continuous_scale=DIVERGING, title="Margin % by Discount Bucket")
        fig.update_layout(height=400, coloraxis_showscale=False, **PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        corr = fdf[["Order Item Discount Rate", "Order Item Profit Ratio"]].corr().iloc[0, 1]
        st.markdown(f"""
        <div class="kpi-card" style="margin-top:12px;">
            <div class="kpi-label">Discount ↔ Profit Ratio Correlation</div>
            <div class="kpi-value">{corr:.3f}</div>
            <div class="section-caption" style="margin-top:8px;">Negative values confirm margin erosion accelerates as discount rate rises.</div>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(
            disc_perf.style.format({"Revenue": "${:,.0f}", "Profit": "${:,.0f}", "Margin %": "{:.1f}%"}),
            use_container_width=True, height=250
        )

    st.markdown('<div class="section-title">What-If Discount Scenario</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-caption">Simulate a uniform discount-rate shift and see the projected margin impact, holding unit economics otherwise constant.</div>', unsafe_allow_html=True)

    scenario_shift = st.slider("Simulated discount rate change (percentage points)", -10.0, 10.0, 0.0, 0.5, format="%.1f") / 100

    sim = fdf.copy()
    sim["Sim Discount Rate"] = (sim["Order Item Discount Rate"] + scenario_shift).clip(0, 1)
    sim["Sim Discount Amount"] = sim["Order Item Product Price"] * sim["Sim Discount Rate"] * sim["Order Item Quantity"]
    sim["Sim Order Item Total"] = (sim["Order Item Product Price"] * sim["Order Item Quantity"]) - sim["Sim Discount Amount"]
    # Approximate benefit shift: assume cost structure fixed, so incremental discount dollars fall straight to profit
    delta_discount_dollars = (sim["Sim Discount Amount"] - sim["Order Item Discount"]).sum()
    sim_profit = total_profit - delta_discount_dollars
    sim_margin = sim_profit / total_revenue * 100 if total_revenue else 0

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Current Profit</div>
        <div class="kpi-value">${total_profit:,.0f}</div></div>""", unsafe_allow_html=True)
    with c2:
        delta_class = "kpi-delta-pos" if sim_profit >= total_profit else "kpi-delta-neg"
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Simulated Profit</div>
        <div class="kpi-value">${sim_profit:,.0f}</div>
        <div class="{delta_class}">{'+' if sim_profit>=total_profit else ''}{sim_profit-total_profit:,.0f} vs current</div></div>""", unsafe_allow_html=True)
    with c3:
        delta_class = "kpi-delta-pos" if sim_margin >= margin_pct else "kpi-delta-neg"
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Simulated Margin</div>
        <div class="kpi-value">{sim_margin:.2f}%</div>
        <div class="{delta_class}">{'+' if sim_margin>=margin_pct else ''}{sim_margin-margin_pct:.2f} pts vs current</div></div>""", unsafe_allow_html=True)

    st.caption("Simulation approximates that every incremental discount dollar reduces profit dollar-for-dollar (cost base held constant). Use as directional guidance, not a pricing model.")

st.markdown("---")
st.caption("APL Logistics (KWE Group) · Unified Mentor Project · Customer, Product & Profitability Performance Analysis in Supply Chain Operations")