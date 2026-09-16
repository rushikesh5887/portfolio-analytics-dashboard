"""
Created on Wed Jan 14 15:31:58 2026

@author: rushikesh
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from babel.numbers import format_decimal


# For Indian Numbering Format
def indian_format(number):
    number = float(number)

    if number < 0:
        return "-₹" + indian_format(abs(number))

    number = round(number)

    s = str(number)

    if len(s) <= 3:
        return "₹" + s

    last_three = s[-3:]
    remaining = s[:-3]

    parts = []

    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]

    if remaining:
        parts.insert(0, remaining)

    return "₹" + ",".join(parts) + "," + last_three

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Portfolio Overview",
    layout="wide"
)

# ============================================================
# DASHBOARD STYLING
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #F7F8FA;
    }

    /* Main content width */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Main title */
    h1 {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #1F2937;
        margin-bottom: 0.3rem;
    }

    /* Section headings */
    h2 {
        font-size: 1.45rem !important;
        font-weight: 650 !important;
        color: #1F2937;
        margin-top: 1.5rem;
    }

    h3 {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: #374151;
    }

    /* KPI cards */
    [data-testid="stMetric"] {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #6B7280 !important;
        font-weight: 500 !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.55rem !important;
        font-weight: 700 !important;
        color: #111827 !important;
    }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Sidebar text */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white !important;
}
    /* Sidebar title */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: white !important;
    }

/* Selectboxes */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: white !important;
    border-radius: 8px;
    border: 1px solid #D1D5DB !important;
}

/* Selected dropdown text */
section[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: #111827 !important;
}
/* Professional blue for selected filter tags */
section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background-color: #2563EB !important;
    color: white !important;
}

/* Filter tag text */
section[data-testid="stSidebar"] span[data-baseweb="tag"] span {
    color: white !important;
}

/* Filter tag remove X */
section[data-testid="stSidebar"] span[data-baseweb="tag"] svg {
    fill: white !important;
}
    /* Dataframes */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #E5E7EB;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        border: 1px solid #D1D5DB;
        font-weight: 500;
    }

    /* Horizontal divider */
    hr {
        border: none;
        border-top: 1px solid #E5E7EB;
        margin: 1.5rem 0;
    }

</style>
""", unsafe_allow_html=True)
# ============================================================
# SIDEBAR - MAIN PAGE SELECTOR
# ============================================================

st.sidebar.header("💡 Portfolio Insights")

analysis_page = st.sidebar.selectbox(
    "Investment Overview",
    ["Overview",
        "Detailed Positions",
        "Investment Trend"
    ]
)


# ============================================================
# PAGE 1 - PORTFOLIO OVERVIEW
# ============================================================

if analysis_page == "Overview":

    st.title("Indian Equity Investments")
    st.caption("Executive overview of portfolio allocation,     performance and asset-class returns")

    # ========================================================
    # LOAD DIRECT EQUITY + GOLD
    # ========================================================

    @st.cache_data
    def load_current_data():
        return pd.read_csv("India_Total_Portfolio.csv")

    df_Equity = load_current_data()

    # --------------------------------------------------------
    # Ensure numeric columns
    # --------------------------------------------------------

    df_Equity["Current_Valuation"] = pd.to_numeric(
        df_Equity["Current_Valuation"],
        errors="coerce"
    )

    df_Equity["Total_Ivestment"] = pd.to_numeric(
        df_Equity["Total_Ivestment"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Clean Asset Group
    # --------------------------------------------------------

    df_Equity["Asset_Group"] = (
        df_Equity["Asset_Group"]
        .astype(str)
        .str.strip()
    )


    # ========================================================
    # GOLD / PRECIOUS METALS
    # ========================================================

    gold_mask = df_Equity["Asset_Group"].str.contains(
        "precious",
        case=False,
        na=False
    )

    gold_value = df_Equity.loc[
        gold_mask,
        "Current_Valuation"
    ].sum()

    gold_investment = df_Equity.loc[
        gold_mask,
        "Total_Ivestment"
    ].sum()

    # ========================================================
    # DIRECT EQUITY
    # ========================================================

    # Everything except Precious Metal
    equity_mask = ~gold_mask

    equity_value = df_Equity.loc[
        equity_mask,
        "Current_Valuation"
    ].sum()

    equity_investment = df_Equity.loc[
        equity_mask,
        "Total_Ivestment"
    ].sum()

    # ========================================================
    # MUTUAL FUNDS
    # ========================================================

    @st.cache_data
    def load_mf_data():
        return pd.read_csv("mutual_funds.csv")

    mutual_funds = load_mf_data()

    mutual_funds["CostValue"] = pd.to_numeric(
        mutual_funds["CostValue"],
        errors="coerce"
    )

    mutual_funds["CurrentValue"] = pd.to_numeric(
        mutual_funds["CurrentValue"],
        errors="coerce"
    )

    mf_investment = mutual_funds["CostValue"].sum()

    mf_value = mutual_funds["CurrentValue"].sum()

    # ========================================================
    # TOTAL PORTFOLIO
    # ========================================================

    total_investment = (
        equity_investment
        + gold_investment
        + mf_investment
    )

    total_value = (
        equity_value
        + gold_value
        + mf_value
    )

    total_pnl = (
        total_value
        - total_investment
    )

    total_return = (
        total_pnl
        / total_investment
        * 100
        if total_investment != 0
        else 0
    )

    # ========================================================
    # VALIDATION
    # ========================================================

    # This should equal the total value in India_Total_Portfolio.csv
    equity_file_total = df_Equity[
        "Current_Valuation"
    ].sum()

    classified_total = (
        equity_value
        + gold_value
    )

    # Uncomment while checking the numbers
    #
    # st.write("Direct Equity:", equity_value)
    # st.write("Gold:", gold_value)
    # st.write("Equity File Total:", equity_file_total)
    # st.write("Equity + Gold:", classified_total)

    # ========================================================
    # KPI SECTION
    # ========================================================

    st.subheader(" ")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Investment",
        indian_format(total_investment)
    )

    col2.metric(
        "Current Value",
        indian_format(total_value)
    )

    col3.metric(
        "Unrealized P&L",
        indian_format(total_pnl),
        delta=f"{total_return:.1f}%"
    )

    col4.metric(
        "Portfolio Return",
        f"{total_return:.1f}%"
    )
    
    # 

    # ========================================================
    # PORTFOLIO ALLOCATION DATA
    # ========================================================

    portfolio_allocation = pd.DataFrame({
        "Asset": [
            "Direct Equity",
            "Gold",
            "Mutual Funds"
        ],
        "Current Value": [
            equity_value,
            gold_value,
            mf_value
        ]
    })

    # ========================================================
    # INVESTMENT VS RETURN DATA
    # ========================================================

    if total_pnl >= 0:

        investment_return = pd.DataFrame({
            "Component": [
                "Investment",
                "Unrealized Return"
            ],
            "Value": [
                total_investment,
                total_pnl
            ]
        })

    else:

        investment_return = pd.DataFrame({
            "Component": [
                "Current Value",
                "Unrealized Loss"
            ],
            "Value": [
                total_value,
                abs(total_pnl)
            ]
        })

    # ========================================================
    # TWO DONUT CHARTS
    # ========================================================

    left, right = st.columns(2)

    # ========================================================
    # DONUT 1 - CURRENT PORTFOLIO ALLOCATION
    # ========================================================

    with left:

        fig_portfolio = px.pie(
            portfolio_allocation,
            names="Asset",
            values="Current Value",
            hole=0.55,
            title="Current Portfolio Allocation",
            color="Asset",
            color_discrete_map={
                "Gold": "#D4AF37",
                "Mutual Funds": "#4CAF50",
                "Direct Equity": "#3B82F6"
                }
        )

        fig_portfolio.update_traces(
            textinfo="label+percent",
            hovertemplate=
                "<b>%{label}</b><br>"
                "Current Value: ₹%{value:,.0f}<br>"
                "Portfolio Weight: %{percent}"
                "<extra></extra>"
        )

        fig_portfolio.update_layout(
            margin=dict(
                t=60,
                l=20,
                r=20,
                b=20
            )
        )

        st.plotly_chart(
            fig_portfolio,
            use_container_width=True
        )

    # ========================================================
    # DONUT 2 - INVESTMENT VS RETURN / LOSS
    # ========================================================

    with right:

        if total_pnl >= 0:

            fig_return = px.pie(
                investment_return,
                names="Component",
                values="Value",
                hole=0.55,
                title="Investment vs Unrealized Return"
            )

        else:

            fig_return = px.pie(
                investment_return,
                names="Component",
                values="Value",
                hole=0.55,
                title="Current Value vs Unrealized Loss",
                color='Component'
            )

        fig_return.update_traces(
            textinfo="label+percent",
            hovertemplate=
                "<b>%{label}</b><br>"
                "Value: ₹%{value:,.0f}<br>"
                "Portfolio Share: %{percent}"
                "<extra></extra>"
        )

        fig_return.update_layout(
            margin=dict(
                t=60,
                l=20,
                r=20,
                b=20
            )
        )

        st.plotly_chart(
            fig_return,
            use_container_width=True
        )
  #      ============================================================
    # INVESTMENT VS CURRENT VALUE BY ASSET CLASS
    # ============================================================
    st.subheader("Performance of Asset Class")
    asset_performance = pd.DataFrame({
        "Asset Class": [
            "Direct Equity",
            "Gold",
            "Mutual Funds"
        ],
        "Invested": [
            equity_investment,
            gold_investment,
            mf_investment
        ],
        "Current Value": [
            equity_value,
            gold_value,
            mf_value
        ]
    })
    
    # Calculate return %
    asset_performance["Return %"] = (
        (asset_performance["Current Value"]
         - asset_performance["Invested"])
        / asset_performance["Invested"]
        * 100
    )
    
    # Convert to long format for grouped bar chart
    asset_plot = asset_performance.melt(
        id_vars=["Asset Class", "Return %"],
        value_vars=["Invested", "Current Value"],
        var_name="Measure",
        value_name="Amount"
    )
    
    
    
    fig_asset = px.bar(
        asset_plot,
        x="Asset Class",
        y="Amount",
        color="Measure",
        barmode="group",
        text_auto=".2s",
        custom_data=["Return %"]
    )
    
    fig_asset.update_traces(
        hovertemplate=
            "<b>%{x}</b><br>"
            "%{fullData.name}: ₹%{y:,.0f}<br>"
            "Return: %{customdata[0]:.1f}%"
            "<extra></extra>"
    )
    
    fig_asset.update_layout(
        xaxis_title="",
        yaxis_title="Amount (₹)",
        legend_title="",
        plot_bgcolor="white",
        hovermode="x unified"
    )
    
    st.plotly_chart(
        fig_asset,
        use_container_width=True
    )
        # # ============================================================
    # ROW 4 — RISK & CONCENTRATION + PORTFOLIO INSIGHTS
    # ============================================================
    
    st.markdown("## Risk & Concentration")
    
    left, right = st.columns(2)
    
    
    # ============================================================
    # CREATE CLEAN EQUITY DATA FOR ROW 4
    # ============================================================
    
    equity_df = df_Equity[~gold_mask].copy()
    
    equity_df["Unrealized_PnL"] = (
        equity_df["Current_Valuation"]
        - equity_df["Total_Ivestment"]
    )
    
    
    # ============================================================
    # LEFT — RISK & CONCENTRATION
    # ============================================================
    
    with left:
    
        total_equity_value = equity_df["Current_Valuation"].sum()
    
        if total_equity_value > 0:
    
            # ----------------------------------------------------
            # Holding concentration
            # ----------------------------------------------------
    
            holding_values = (
                equity_df
                .groupby("Symbol")["Current_Valuation"]
                .sum()
                .sort_values(ascending=False)
            )
    
            top5_weight = (
                holding_values.head(5).sum()
                / total_equity_value
                * 100
            )
    
            largest_holding = (
                holding_values.iloc[0]
                / total_equity_value
                * 100
            )
    
            largest_holding_name = holding_values.index[0]
    
    
            # ----------------------------------------------------
            # Sector concentration
            # ----------------------------------------------------
    
            sector_values = (
                equity_df
                .groupby("Sector")["Current_Valuation"]
                .sum()
                .sort_values(ascending=False)
            )
    
            largest_sector = (
                sector_values.iloc[0]
                / total_equity_value
                * 100
            )
    
            largest_sector_name = sector_values.index[0]
    
    
            # ----------------------------------------------------
            # KPI display
            # ----------------------------------------------------
    
            r1, r2, r3 = st.columns(3)
    
            r1.metric(
                "Top 5 Holdings",
                f"{top5_weight:.1f}%"
            )
    
            r2.metric(
                "Largest Holding",
                f"{largest_holding:.1f}%"
            )
    
            r3.metric(
                "Largest Sector",
                f"{largest_sector:.1f}%"
            )
    
            st.caption(
                f"Largest holding: {largest_holding_name}  •  "
                f"Largest sector: {largest_sector_name}"
            )
    
        else:
    
            st.info("No equity data available.")
    
    
    # ============================================================
    # RIGHT — PORTFOLIO INSIGHTS
    # ============================================================
    
    with right:
    
        st.markdown("### Portfolio Insights")
    
        # --------------------------------------------------------
        # Profitable / loss-making holdings
        # --------------------------------------------------------
    
        profitable = (
            equity_df["Unrealized_PnL"] > 0
        ).sum()
    
        loss_making = (
            equity_df["Unrealized_PnL"] < 0
        ).sum()
    
        total_holdings = profitable + loss_making
    
        if total_holdings > 0:
    
            profitable_pct = (
                profitable
                / total_holdings
                * 100
            )
    
            # ----------------------------------------------------
            # Largest gain
            # ----------------------------------------------------
    
            largest_gain = equity_df.loc[
                equity_df["Unrealized_PnL"].idxmax()
            ]
    
            # ----------------------------------------------------
            # Largest loss
            # ----------------------------------------------------
    
            largest_loss = equity_df.loc[
                equity_df["Unrealized_PnL"].idxmin()
            ]
    
    
            # ----------------------------------------------------
            # Insights
            # ----------------------------------------------------
    
            st.markdown(
                f"🟢 **{profitable_pct:.0f}% of holdings are profitable** "
                f"({profitable} of {total_holdings})."
            )
    
            st.markdown(
                f"📈 **Largest gain:** "
                f"{largest_gain['Symbol']} "
                f"(₹{largest_gain['Unrealized_PnL']:,.0f})"
            )
    
            st.markdown(
                f"📉 **Largest loss:** "
                f"{largest_loss['Symbol']} "
                f"(₹{largest_loss['Unrealized_PnL']:,.0f})"
            )


# ============================================================
# PAGE 2 - CURRENT Eqity
# ============================================================    
elif analysis_page == "Detailed Positions":

    st.title("📊 Direct Equity Portfolio")

    # --------------------------------------------------------
    # Load current portfolio data
    # --------------------------------------------------------

    @st.cache_data
    def load_current_data():
        return pd.read_csv(
            "India_Total_Portfolio.csv"
        )

    df = load_current_data()
    

    # --------------------------------------------------------
    # Ensure numeric
    # --------------------------------------------------------

    numeric_cols = [
        "Total_Ivestment",
        "Current_Valuation"
    ]

    for col in numeric_cols:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # --------------------------------------------------------
    # Compute P&L if not present
    # --------------------------------------------------------

    if "Unrealized_PnL" not in df.columns:

        df["Unrealized_PnL"] = (
            df["Current_Valuation"]
            - df["Total_Ivestment"]
        )

    # --------------------------------------------------------
    # Sidebar filters
    # --------------------------------------------------------

    st.sidebar.header("Filters")

    asset_filter = st.sidebar.multiselect(
        "Asset Group",
        options=df["Asset_Group"].unique(),
        default=df["Asset_Group"].unique()
    )

    sector_filter = st.sidebar.multiselect(
        "Sector",
        options=df["Sector"].unique(),
        default=df["Sector"].unique()
    )

    # --------------------------------------------------------
    # Filter data
    # --------------------------------------------------------

    filtered_df = df[
        (df["Asset_Group"].isin(asset_filter)) &
        (df["Sector"].isin(sector_filter))
    ]

    # ========================================================
    # KPIs
    # ========================================================

    col1, col2, col3,col4 = st.columns(4)

    col1.metric(
        "Total Investment (₹)",
        indian_format(filtered_df['Total_Ivestment'].sum())
    )

    col2.metric(
        "Current Valuation (₹)",
        indian_format(filtered_df['Current_Valuation'].sum())

    )

    pnl = filtered_df["Unrealized_PnL"].sum()

    col3.metric(
        "Unrealized P&L (₹)",
        indian_format(filtered_df['Unrealized_PnL'].sum()),
        delta=f"{pnl:,.0f}"
    )
    pnl_perc = (filtered_df["Unrealized_PnL"].sum())/      (filtered_df['Total_Ivestment'].sum())*100
    
    col4.metric(
        "Unrealized P&L (%)",
        f"{pnl_perc:,.0f}%",
        delta=f"{pnl_perc:,.0f}%"
    )
    
    # ========================================================
    # SECTOR-WISE SUMMARY
    # ========================================================

    sector_summary = (
        filtered_df
        .groupby("Sector", as_index=False)
        .agg(
            Total_Investment=(
                "Total_Ivestment",
                "sum"
            ),
            Current_Valuation=(
                "Current_Valuation",
                "sum"
            ),
            Unrealized_PnL=(
                "Unrealized_PnL",
                "sum"
            )
        )
    )

    sector_summary["Return_%"] = (
        sector_summary["Unrealized_PnL"]
        / sector_summary["Total_Investment"]
        * 100
    )

    total_portfolio_value = (
        sector_summary["Current_Valuation"].sum()
    )

    sector_summary["Weight_%"] = (
        sector_summary["Total_Investment"]
        / total_portfolio_value
        * 100
    )

    # ========================================================
    # SUNBURST
    # ========================================================

    st.subheader(
        "Portfolio Allocation – Sector & Stock Breakdown"
    )

    value_choice = st.radio(
        "Show allocation by:",
        options=[
            "Total Investment",
            "Current Valuation"
        ],
        horizontal=True
    )

    sunburst_df = filtered_df.copy()

    if value_choice == "Total Investment":

        sunburst_df["Value"] = (
            sunburst_df["Total_Ivestment"]
        )

    else:

        sunburst_df["Value"] = (
            sunburst_df["Current_Valuation"]
        )

    sunburst_df = (
        sunburst_df[
            ["Sector", "Symbol", "Value"]
        ]
        .dropna()
    )

    fig_sunburst = px.sunburst(
        sunburst_df,
        path=[
            "Sector",
            "Symbol"
        ],
        values="Value",
        color="Sector",
        color_discrete_sequence=(
            px.colors.qualitative.Bold
        )
    )

    fig_sunburst.update_traces(
        textinfo="label+percent parent",
        insidetextorientation="radial",
        marker=dict(
            line=dict(
                color="white",
                width=1
            )
        ),
        texttemplate=(
            "%{label}<br>%{percentParent:.1%}"
        )
    )

    fig_sunburst.update_layout(
        margin=dict(
            t=40,
            l=0,
            r=0,
            b=0
        )
    )

    st.plotly_chart(
        fig_sunburst,
        use_container_width=True
    )

    # ========================================================
    # SECTORAL P&L BAR CHARTS
    # ========================================================

    left, right = st.columns(2)

    # ========================================================
    # ROW 1 - INVESTMENT VS VALUATION
    # ========================================================

    with left:

        fig_alloc = px.bar(
            sector_summary,
            x="Sector",
            y=[
                "Total_Investment",
                "Current_Valuation"
            ],
            barmode="group",
            title="Investment vs Current Valuation"
        )

        fig_alloc.update_layout(
            yaxis=dict(
                zeroline=True,
                zerolinecolor="black",
                title="Investment in ₹"
            ),
            xaxis=dict(
                title="Sector",
                tickangle=-30,
                categoryorder="total ascending"
            ),
            template="plotly_white"
        )

        st.plotly_chart(
            fig_alloc,
            use_container_width=True
        )

    # ========================================================
    # ROW 1 - SECTOR WEIGHT
    # ========================================================

    with right:

        fig_sector_weight = px.bar(
            sector_summary,
            x="Sector",
            y="Weight_%",
            color="Sector",
            title="Sector-wise Investment Allocation (%)",
            text=(
                sector_summary["Weight_%"]
                .round(1)
                .astype(str)
                + "%"
            ),
            category_orders={
                "Sector":
                sector_summary
                .sort_values("Weight_%")
                ["Sector"]
            }
        )

        fig_sector_weight.update_traces(
            textposition="outside",
            cliponaxis=False,
            width=0.6
        )

        fig_sector_weight.update_layout(
            yaxis=dict(
                title="Portfolio Weight (%)",
                zeroline=True,
                zerolinecolor="black"
            ),
            xaxis=dict(
                title="Sector",
                tickangle=-30,
                categoryorder="total ascending"
            ),
            template="plotly_white",
            showlegend=False,
            bargap=0.25
        )

        st.plotly_chart(
            fig_sector_weight,
            use_container_width=True
        )

    # ========================================================
    # ROW 2 - SECTOR RETURNS
    # ========================================================

    sector_summary["PnL_Flag"] = (
        sector_summary["Return_%"]
        .apply(
            lambda x:
            "Profit" if x >= 0 else "Loss"
        )
    )

    with left:

        fig_sector_pct = px.bar(
            sector_summary,
            x="Sector",
            y="Return_%",
            color="PnL_Flag",
            color_discrete_map={
                "Profit": "green",
                "Loss": "red"
            },
            title="Sector-wise Return (%)",
            text=(
                sector_summary["Return_%"]
                .round(1)
                .astype(str)
                + "%"
            ),
            category_orders={
                "Sector":
                sector_summary
                .sort_values("Return_%")
                ["Sector"]
            }
        )

        fig_sector_pct.update_traces(
            textposition="outside",
            cliponaxis=False,
            width=0.6
        )

        fig_sector_pct.update_layout(
            yaxis=dict(
                title="Return (%)",
                zeroline=True,
                zerolinecolor="black"
            ),
            xaxis=dict(
                title="Sector",
                tickangle=-30
            ),
            template="plotly_white",
            showlegend=False,
            bargap=0.25
        )

        fig_sector_pct.add_hline(
            y=0,
            line_dash="dot",
            line_color="black"
        )

        st.plotly_chart(
            fig_sector_pct,
            use_container_width=True
        )

    # ========================================================
    # ROW 2 - SECTOR P&L AMOUNTS
    # ========================================================

    sector_summary["PnL_Flag_Value"] = (
        sector_summary["Unrealized_PnL"]
        .apply(
            lambda x:
            "Profit" if x >= 0 else "Loss"
        )
    )

    with right:

        fig_pnl = px.bar(
            sector_summary,
            x="Sector",
            y="Unrealized_PnL",
            color="PnL_Flag_Value",
            color_discrete_map={
                "Profit": "green",
                "Loss": "red"
            },
            title="Unrealized P&L by Sector",
            text_auto=".2s",
            category_orders={
                "Sector":
                sector_summary
                .sort_values("Unrealized_PnL")
                ["Sector"]
            }
        )

        fig_pnl.update_traces(
            width=0.6,
            textposition="outside",
            cliponaxis=False
        )

        fig_pnl.update_layout(
            yaxis=dict(
                zeroline=True,
                zerolinecolor="black",
                title="Unrealized P&L (₹)"
            ),
            xaxis=dict(
                title="Sector",
                tickangle=-30
            ),
            template="plotly_white",
            showlegend=False,
            bargap=0.25
        )

        fig_pnl.add_hline(
            y=0,
            line_dash="dot",
            line_color="black"
        )

        st.plotly_chart(
            fig_pnl,
            use_container_width=True
        )
    # ============================================================
# TOP 10 UNREALIZED GAINS
# ============================================================
    with left:
        top10_unrealized = (
            df[df["Unrealized_PnL"] > 0]
            .sort_values("Unrealized_PnL", ascending=False)
            .head(10)
        )
        
        top10_unrealized["Gain_Percentage"] = (
            top10_unrealized["Unrealized_PnL"]
            / top10_unrealized["Total_Ivestment"]* 100)
        
        top10_unrealized = (
            top10_unrealized
            .sort_values("Unrealized_PnL", ascending=False)
            .head(10))
        
        top10_unrealized["Label"] = top10_unrealized.apply(
            lambda row: f"₹{row['Unrealized_PnL']:,.0f}             <br>({row['Gain_Percentage']:.1f}%)",
    axis=1)
        
        fig = px.bar(
            top10_unrealized,
            x="Symbol",
            y="Unrealized_PnL",
            text="Label",
            title="Top 10 Unrealized Gains"
        )
        
        fig.update_traces(
                          textfont=dict(size=16),
                          textposition="outside")
        
        fig.update_layout(
            xaxis_title="Stock",
            yaxis_title="Unrealized P&L (₹)",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(
            fig,
            use_container_width=True
        )
        
        # ============================================================
# TOP 10 UNREALIZED LOSSES
# ============================================================
    with right:
        top10_losses = (
            df[df["Unrealized_PnL"] < 0]
            .copy()
        )
        
        top10_losses["Loss_Percentage"] = (
            top10_losses["Unrealized_PnL"]
            / top10_losses["Total_Ivestment"] * 100
        )
        
        top10_losses = (
            top10_losses
            .sort_values("Unrealized_PnL", ascending=True)
            .head(10)
        )
        
        top10_losses["Label"] = top10_losses.apply(
            lambda row:
            f"₹{row['Unrealized_PnL']:,.0f}<br>"
            f"({row['Loss_Percentage']:.1f}%)",
            axis=1
        )
        
        fig = px.bar(
            top10_losses,
            x="Symbol",
            y="Unrealized_PnL",
            text="Label",
            title="Top 10 Unrealized Losses"
        )
        
        fig.update_traces(
            textfont=dict(size=16),
            textposition="outside"
        )
        
        fig.update_layout(
            xaxis_title="Stock",
            yaxis_title="Unrealized P&L (₹)",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(
            fig,
            use_container_width=True
        )
    # ========================================================
    # ROW 3 - TREEMAP
    # ========================================================

    st.subheader(
        "P&L Stock Level Breakdown"
    )

    treemap_df = filtered_df.copy()

    treemap_df["Abs_PnL"] = (
        treemap_df["Unrealized_PnL"].abs()
    )

    fig_tree = px.treemap(
        treemap_df,
        path=[
            "Sector",
            "Symbol"
        ],
        values="Abs_PnL",
        color="Unrealized_PnL",
        color_continuous_scale=[
            "red",
            "white",
            "green"
        ],
        color_continuous_midpoint=0
    )

    st.plotly_chart(
        fig_tree,
        use_container_width=True
    )
    # ========================================================
    # Mutual Funds
    # ========================================================
    st.subheader(
        "Mutual Fund Breakdown"
    )
    
    # ========================================================
    # LOAD MF data
    # ========================================================
    @st.cache_data
    def load_mf_data():
        return pd.read_csv('mutual_funds.csv')
        
    mutual_funds = load_mf_data()
    # ========================================================
    # KPIs
    # ========================================================

    col1, col2, col3,col4, = st.columns(4)

    col1.metric(
        "Total Investment (₹)",
        indian_format(mutual_funds['CostValue'].sum())
    )

    col2.metric(
        "Current Valuation (₹)",
        indian_format(mutual_funds['CurrentValue'].sum())
    )

    mf_pnl = mutual_funds["Appreciation"].sum()
    
    return_pct = (mf_pnl / mutual_funds['CostValue'].sum())*100
    
    col3.metric(
        "Current Capital Gain (₹)",
        indian_format(mf_pnl),
        delta=f"{return_pct:,.1f}%"
    )

    # # ------------------------------------------------
    # # Current SIP
    # # ------------------------------------------------

    sip_funds = mutual_funds[
         mutual_funds["SIP"] > 0
     ]
    
    sip_amount = sip_funds["SIP"].sum()
    
    sip_names = " | ".join(
    f"{row['Scheme']}: ₹{row['SIP']:,.0f}"
    for _, row in sip_funds.iterrows())
    
    col4.metric(
         "Current Total Monthly SIP",
         indian_format(sip_amount),
         delta= sip_names
     )

   # Calculate Weighted XIRR for each group
    weighted_xirr_dict = (
            mutual_funds
            .groupby("Market Cap")
            .apply(
                lambda x: (
                    x["XIRR"] * x["CurrentValue"]
                ).sum() / x["CurrentValue"].sum()
            )
            .to_dict()
        )

        # ------------------------------------------------
        # Create Basic Sunburst
        # ------------------------------------------------
    risk_colors = {
    "Hybrid": "#66BB6A",
    "Mid Cap": "#FFD54F",
    "Small & Mid Cap": "#FFB74D",
    "Small Cap": "#EE6363"
}
    
    fig_mf = px.sunburst(
            mutual_funds,
            path=["Market Cap", "Scheme"],
            color="Market Cap",
            color_discrete_map= risk_colors,
            values="CurrentValue",
            title="Mutual Fund Portfolio"
        )
    # ------------------------------------------------
    # Create text for every Sunburst node
    # ------------------------------------------------

    text = []

    for label in fig_mf.data[0].labels:

        if label in weighted_xirr_dict:

            # Inner Market Cap circle
            text.append(
                f"{label}<br>"
                f"XIRR: {weighted_xirr_dict[label]:.1f}%"
            )

        else:

            # Scheme level
            row = mutual_funds[
                mutual_funds["Scheme"] == label
            ]

            if not row.empty:
                xirr = row["XIRR"].iloc[0]

                text.append(
                    f"{label}<br>"
                    f"XIRR: {xirr:.1f}%"
                )
            else:
                text.append(label)

    fig_mf.update_traces(
        text=text,
        textinfo="text+percent parent",
        insidetextorientation="radial",
        marker=dict(
            line=dict(
                color="white",
                width=1
            )
        )
    )
    fig_mf.update_layout(
        margin=dict(
            t=40,
            l=0,
            r=0,
            b=0
        )
    )
    st.plotly_chart(
            fig_mf,
            use_container_width=True
        )

    # ========================================================
    # MUTUAL FUND — INVESTMENT VS CURRENT VALUE
    # ========================================================
    
    mf_plot = mutual_funds[
        ["Scheme", "CostValue", "CurrentValue", "Appreciation"]
    ].copy()
    
    # Rename columns for the legend
    mf_plot = mf_plot.rename(columns={
        "CostValue": "Invested",
        "CurrentValue": "Current Valuation"
    })
    
    fig_mf_performance = px.bar(
        mf_plot,
        x="Scheme",
        y=["Invested", "Current Valuation"],
        barmode="group",
        title="Mutual Fund Investment vs Current Valuaton",
        labels={
            "value": "Amount (₹)",
            "variable": ""
        }
    )
    
    # Show amount on top of each bar
    fig_mf_performance.update_traces(
        texttemplate="₹%{y:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>%{fullData.name}: ₹%{y:,.0f}<extra></extra>"
    )
    
    fig_mf_performance.update_traces(
        hovertemplate=
            "<b>%{x}</b><br>"
            "%{fullData.name}: ₹%{y:,.0f}"
            "<extra></extra>"
    )
    
    fig_mf_performance.update_layout(
        xaxis_title="",
        yaxis_title="Amount (₹)",
        legend_title="",
        plot_bgcolor="white",
        hovermode="x unified",
        margin=dict(
            t=60,
            l=20,
            r=20,
            b=20
        )
    )
    
    st.plotly_chart(
        fig_mf_performance,
        use_container_width=True
    )
# ============================================================
# PAGE 2 -Investment Trend
# ============================================================

elif analysis_page == "Investment Trend":

    st.title("Investment Trend in Direct Equities")

    # ========================================================
    # LOAD HISTORICAL LEDGER
    # ========================================================

    @st.cache_data
    def load_historical_data():

        return pd.read_csv(
            "ledger-ZJ5852.csv"
        )
    investment_ledger = load_historical_data()

    # ========================================================
    # MONEY ADDED TO PORTFOLIO
    # ========================================================

    prefixes = (
        'Being amount received from',
        'Funds added using payment gateway from',
        'Funds added using UPI'
    )

    poured_money = investment_ledger[
        investment_ledger[
            'particulars'
        ].str.startswith(
            prefixes,
            na=False
        )
    ].copy()

    poured_money['Invested_Lakh'] = (
        poured_money['credit'] / 1e5
    )

    # ========================================================
    # MONEY TRANSFERRED BACK
    # ========================================================

    prefixes_reverse = (
        'Funds transferred back',
        'Payout of '
    )

    reversed_money = investment_ledger[
        investment_ledger[
            'particulars'
        ].str.startswith(
            prefixes_reverse,
            na=False
        )
    ].copy()

    reversed_money = reversed_money[
        (reversed_money['debit'] > 0) &
        (
            reversed_money['voucher_type']
            == 'Bank Payments'
        )
    ]

    reversed_money['Invested_Lakh'] = (
        -reversed_money['debit'] / 1e5
    )

    reversed_money['Correction_Flag'] = True

    # Original investments
    poured_money['Correction_Flag'] = False

    # ========================================================
    # COMBINE
    # ========================================================

    poured_money = pd.concat(
        [
            poured_money,
            reversed_money
        ],
        ignore_index=True
    )

    # ========================================================
    # SORT BY DATE
    # ========================================================

    poured_money['posting_date'] = pd.to_datetime(
        poured_money['posting_date'],
        errors="coerce"
    )

    poured_money = (
        poured_money
        .sort_values("posting_date")
        .reset_index(drop=True)
    )

    # ========================================================
    # CUMULATIVE INVESTMENT
    # ========================================================

    poured_money[
        'Cumulative_Investment_Lakh'
    ] = (
        poured_money['Invested_Lakh']
        .cumsum()
    )

    # ========================================================
    # KPI
    # ========================================================

    total_investment = (
        poured_money['Invested_Lakh'].sum()
    )
    yearly_input = (total_investment / (2026-2017))
    col1, col2 = st.columns(2)

    col1.metric(
        "Net Investment",
        f"₹{total_investment:,.2f} L"
    )

    col2.metric(
        "Yearly Average Investment ",
        f"₹{yearly_input:,.2f} L"
    )

    # ========================================================
    # CUMULATIVE INVESTMENT LINE
    # ========================================================

    st.subheader(
        "Cumulative Investments"
    )

    fig_cumulative = px.line(
        poured_money,
        x='posting_date',
        y='Cumulative_Investment_Lakh',
        title=' ',
        markers=True,
        hover_data={
            'posting_date': '|%d-%b-%Y',
            'Invested_Lakh': ':.2f',
            'Cumulative_Investment_Lakh': ':.2f'
        }
    )

    fig_cumulative.update_layout(
        xaxis_title='Date',
        yaxis_title='Investment (₹ Lakh)',
        plot_bgcolor='white',
        hovermode='x unified',
        title=dict(
            x=0.5,
            xanchor='center',
            font=dict(
                size=20,
                family='Arial'
            )
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgrey',
            tickangle=-45
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgrey'
        ),
        margin=dict(
            l=50,
            r=50,
            t=80,
            b=80
        )
    )

    fig_cumulative.update_traces(
        line=dict(
            color='royalblue',
            width=3
        ),
        marker=dict(
            size=8,
            color=poured_money[
                'Correction_Flag'
            ].map({
                False: 'green',
                True: 'red'
            })
        ),
        customdata=poured_money[
            [
                'Invested_Lakh',
                'Correction_Flag'
            ]
        ],
        hovertemplate='<b>Date:</b> %{x|%d-%b-%Y}<br>'
        '<b>Cumulative:</b> ₹%{y:.2f} L<br>'
        '<b>Invested:</b> ₹%{customdata[0]:.2f} L<br>'
        '<b>Correction:</b> %{customdata[1]}'
        '<extra></extra>'
    )

    st.plotly_chart(
        fig_cumulative,
        use_container_width=True
    )

    # ========================================================
    # YEARLY INVESTMENT
    # ========================================================

    poured_money['Year'] = (
        poured_money['posting_date'].dt.year
    )

    yearly = (
        poured_money
        .groupby(
            'Year',
            as_index=False
        )['Invested_Lakh']
        .sum()
    )

    yearly['Invested_Lakh_Total'] = (
        yearly['Invested_Lakh']
    )


# ========================================================
# YEARLY INVESTMENT BAR CHART
# #========================================================

    st.subheader(
        "Yearly Equity Investment"
    )

    fig_yearly = px.bar(
        yearly,
        x='Year',
        y='Invested_Lakh_Total',
        title='Yearly Investment',
        text='Invested_Lakh_Total'
    )

    # Beautify
    fig_yearly.update_traces(
        texttemplate='₹%{text:.2f} L',
        textposition='outside',
        hovertemplate='Year: %{x}<br>'
        'Investment: ₹%{y:.2f} L'
        '<extra></extra>'
    )

    fig_yearly.update_layout(
        xaxis_title='Year',
        yaxis_title='Total Investment (₹ Lakh)',
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        xaxis=dict(
            tickmode='linear',
            dtick=1
        ),
        plot_bgcolor='white'
    )

    fig_yearly.update_yaxes(
        tickformat=','
    )

    st.plotly_chart(
        fig_yearly,
        use_container_width=True
    )
    # ============================================================
    # YEARLY DIVIDEND
    # ============================================================

    st.subheader("💰 Dividend Summary")

    @st.cache_data
    def load_dividend_data():
        return pd.read_csv("final_div_ledger.csv")

    final_div_ledger = load_dividend_data()

    final_div_ledger['Ex-Date'] = pd.to_datetime(
        final_div_ledger['Ex-Date']
    )

    final_div_ledger['Net Dividend Amount'] = pd.to_numeric(
        final_div_ledger['Net Dividend Amount'],
        errors='coerce'
    )

    final_div_ledger = final_div_ledger.dropna(
        subset=['Ex-Date', 'Net Dividend Amount']
    )

    final_div_ledger['Year'] = (
        final_div_ledger['Ex-Date'].dt.year
    )

    # Step 4.1
    yearly_stock_div = (
        final_div_ledger
        .groupby(
            ['Year', 'Symbol'],
            as_index=False
        )['Net Dividend Amount']
        .sum()
    )

    # Step 4.2
    top3_each_year = (
        yearly_stock_div
        .sort_values(
            ['Year', 'Net Dividend Amount'],
            ascending=[True, False]
        )
        .groupby('Year')
        .head(3)
    )

    # Step 4.3
    yearly_total = (
        yearly_stock_div
        .groupby(
            'Year',
            as_index=False
        )['Net Dividend Amount']
        .sum()
    )

    top3_mask = (
        yearly_stock_div
        .set_index(['Year', 'Symbol'])
        .index
        .isin(
            top3_each_year
            .set_index(['Year', 'Symbol'])
            .index
        )
    )

    yearly_stock_div['Symbol'] = (
        yearly_stock_div.apply(
            lambda row:
            row['Symbol']
            if (
                (row['Year'], row['Symbol'])
                in top3_each_year
                .set_index(['Year', 'Symbol'])
                .index
            )
            else 'Others',
            axis=1
        )
    )

    # Step 4.4
    plot_df = (
        yearly_stock_div
        .groupby(
            ['Year', 'Symbol'],
            as_index=False
        )['Net Dividend Amount']
        .sum()
    )

    # Step 4.5
    plot_df['Year'] = (
        plot_df['Year'].astype(str)
    )

    plot_df['text_label'] = plot_df.apply(
        lambda row:
        f"{row['Symbol']}: ₹{row['Net Dividend Amount']:.2f}",
        axis=1
    )

    plot_df['Symbol'] = (
        plot_df['Symbol'].astype(str)
    )

    plot_df['Year'] = (
        plot_df['Year'].astype(str)
    )

    plot_df['hover_text'] = plot_df.apply(
        lambda r:
        f"Year: {r['Year']}<br>"
        f"Stock: {r['Symbol']}<br>"
        f"Dividend: ₹{r['Net Dividend Amount']:.2f}",
        axis=1
    )

    # Step 5
    TOP3_COLORS = [
        "#2E86AB",
        "#F18F01",
        "#6A994E"
    ]

    OTHERS_COLOR = "#CED4DA"

    plot_df["Rank"] = (
        plot_df
        .groupby("Year")["Net Dividend Amount"]
        .rank(
            method="first",
            ascending=False
        )
    )

    def color_bucket(row):

        if row["Rank"] == 1:
            return "Top 1"

        elif row["Rank"] == 2:
            return "Top 2"

        elif row["Rank"] == 3:
            return "Top 3"

        else:
            return "Others"

    plot_df["Color_Group"] = (
        plot_df.apply(
            color_bucket,
            axis=1
        )
    )

    color_map = {
        "Top 1": TOP3_COLORS[0],
        "Top 2": TOP3_COLORS[1],
        "Top 3": TOP3_COLORS[2],
        "Others": OTHERS_COLOR
    }

    STACK_ORDER = [
        "Top 1",
        "Top 2",
        "Top 3",
        "Others"
    ]

# ============================================================
# STACKED BAR - FORCE ALL COMPONENTS INTO SAME BAR
# ============================================================
    
    fig = go.Figure()
    for group in STACK_ORDER:
        temp = plot_df[
            plot_df["Color_Group"] == group
        ].copy()
    
        fig.add_trace(
            go.Bar(
                x=temp["Year"],
                y=temp["Net Dividend Amount"],
    
                name=group,
    
                marker=dict(
                    color=color_map[group]
                ),
    
                text=temp["Net Dividend Amount"],
    
                texttemplate="₹%{text:,.0f}",
    
                textposition="inside",
    
                customdata=temp[["Symbol"]],
    
                hovertemplate="Stock: %{customdata[0]}<br>"
                "Dividend: ₹%{y:,.2f}"
                "<extra></extra>",
    
                # =================================================
                # THIS IS THE IMPORTANT PART
                # =================================================
                offsetgroup="yearly_dividend",
    
                alignmentgroup="yearly_dividend"
            )
        )
    
    
    # ============================================================
    # LAYOUT
    # ============================================================
    
        fig.update_layout(
    
            barmode="stack",
    
            title="Yearly Dividend",
    
            xaxis=dict(
                type="category",
                title="Year",
                categoryorder="category ascending"
            ),
    
            yaxis=dict(
                title="Total Dividend",
                showline=True,
                linewidth=2,
                linecolor="black",
                mirror=False,
                zeroline=True,
                zerolinecolor="black"
            ),
    
            uniformtext_minsize=12,
    
            uniformtext_mode="hide",
    
            showlegend=False,
    
            plot_bgcolor="white"
        )
    
    
    
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ============================================================
    # YEARLY REALIZED VS UNREALIZED P&L
    # ============================================================
    st.subheader("💰 Capital Gains")
    @st.cache_data
    def load_pnl_data():
        return pd.read_csv("final_pnl_ledger.csv")
    final_pnl_ledger = load_pnl_data()
    # ------------------------------------------------------------
        # 1. Ensure correct datatypes
        # ------------------------------------------------------------
    
    final_pnl_ledger["Year"] = (
            pd.to_numeric(
                final_pnl_ledger["Year"],
                errors="coerce"
            )
        )
    
    final_pnl_ledger["Realized P&L"] = (
            pd.to_numeric(
                final_pnl_ledger["Realized P&L"],
                errors="coerce"
            )
        )
    
    final_pnl_ledger["Unrealized P&L"] = (
            pd.to_numeric(
                final_pnl_ledger["Unrealized P&L"],
                errors="coerce"
            )
        )
    
        # ------------------------------------------------------------
        # Remove rows without a year
        # ------------------------------------------------------------
    
    final_pnl_ledger = final_pnl_ledger.dropna(
            subset=["Year"]
        )
    
    final_pnl_ledger["Year"] = (
            final_pnl_ledger["Year"].astype(int)
        )
    
        # ============================================================
        # 2. YEARLY AGGREGATION
        # ============================================================
    
    yearly_pnl = (
            final_pnl_ledger
            .groupby("Year")[
                [
                    "Realized P&L",
                    "Unrealized P&L"
                ]
            ]
            .sum()
            .reset_index()
        )
    
        # ============================================================
        # 3. YEARLY REALIZED VS UNREALIZED
        # ============================================================
    
    fig1 = px.bar(
            yearly_pnl,
            x="Year",
            y=[
                "Realized P&L",
                "Unrealized P&L"
            ],
            barmode="group",
            title="Yearly Realized vs Unrealized P&L"
        )
    
    fig1.update_layout(
            xaxis_title="Year",
            yaxis_title="P&L (₹)",
            plot_bgcolor="white"
        )
    
    st.plotly_chart(
            fig1,
            use_container_width=True
        )
    
        # ============================================================
        # 4. TOP 10 BEST WINS
        # ============================================================
    
    best_wins = (
            final_pnl_ledger
            .groupby(
                "Symbol",
                as_index=False
            )["Realized P&L"]
            .sum()
            .sort_values(
                "Realized P&L",
                ascending=False
            )
            .head(10)
        )
    
    fig2 = px.bar(
            best_wins,
            x="Symbol",
            y="Realized P&L",
            title="Top 10 Best Wins"
        )
    
    fig2.update_layout(
            xaxis_title="Symbol",
            yaxis_title="Realized P&L (₹)",
            plot_bgcolor="white"
        )
    
    st.plotly_chart(
            fig2,
            use_container_width=True
        )
    
        # ============================================================
        # 5. TOP 10 BIGGEST LOSSES
        # ============================================================
    
    big_fails = (
            final_pnl_ledger
            .groupby(
                "Symbol",
                as_index=False
            )["Realized P&L"]
            .sum()
            .sort_values(
                "Realized P&L",
                ascending=True
            )
            .head(10)
        )
    
    fig3 = px.bar(
            big_fails,
            x="Symbol",
            y="Realized P&L",
            title="Top 10 Big Fails"
        )
    
    fig3.update_layout(
            xaxis_title="Symbol",
            yaxis_title="Realized P&L (₹)",
            plot_bgcolor="white"
        )
    
    st.plotly_chart(
            fig3,
            use_container_width=True
        )
