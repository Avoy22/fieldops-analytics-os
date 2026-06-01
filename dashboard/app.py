"""
Streamlit Executive Dashboard for FieldOps Analytics OS.

This dashboard reads from:
- data/processed/fieldops.db

Run:
streamlit run dashboard/app.py
"""

from pathlib import Path
import sqlite3
import sys

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.bootstrap_data import ensure_database_exists


DB_PATH = PROJECT_ROOT / "data" / "processed" / "fieldops.db"
SQL_DIR = PROJECT_ROOT / "sql"

ensure_database_exists(DB_PATH)

REQUIRED_TABLES = {
    "buyers",
    "providers",
    "work_orders",
    "payments",
    "reviews",
    "support_tickets",
}


st.set_page_config(
    page_title="FieldOps Analytics OS",
    page_icon=":bar_chart:",
    layout="wide",
)


def format_currency(value: float | int | None) -> str:
    """Format a number as whole-dollar currency."""
    if pd.isna(value):
        return "$0"
    return f"${value:,.0f}"


def format_percent(value: float | int | None) -> str:
    """Format a percentage value."""
    if pd.isna(value):
        return "0.0%"
    return f"{value:.1f}%"


def format_days(value: float | int | None) -> str:
    """Format a day count for KPI cards."""
    if pd.isna(value):
        return "0.0 days"
    return f"{value:.1f} days"


def validate_database() -> None:
    """Show a friendly message if the SQLite database is missing or incomplete."""
    if not DB_PATH.exists():
        st.error("SQLite database not found.")
        st.info(f"Expected database path: `{DB_PATH}`")
        st.code(
            "python src/generate_data.py\n"
            "python src/load_to_sqlite.py\n"
            "streamlit run dashboard/app.py",
            language="bash",
        )
        st.stop()

    with sqlite3.connect(DB_PATH) as connection:
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type = 'table';",
            connection,
        )["name"].tolist()

    missing_tables = sorted(REQUIRED_TABLES - set(tables))
    if missing_tables:
        st.error("The database exists, but it is missing required tables.")
        st.write("Missing tables:", ", ".join(missing_tables))
        st.code("python src/load_to_sqlite.py", language="bash")
        st.stop()


def read_sql(query: str) -> pd.DataFrame:
    """Read a SQL query from the FieldOps SQLite database."""
    with sqlite3.connect(DB_PATH) as connection:
        return pd.read_sql_query(query, connection)


def read_sql_file(filename: str) -> str:
    """Read a SQL file from the project sql folder."""
    return (SQL_DIR / filename).read_text(encoding="utf-8")


@st.cache_data(show_spinner=False)
def load_overview_metrics() -> pd.DataFrame:
    query = """
    SELECT
        COUNT(*) AS total_work_orders,
        SUM(CASE WHEN status IN ('completed', 'approved') THEN 1 ELSE 0 END) AS successful_orders,
        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
        ROUND(SUM(total_amount), 2) AS gross_work_order_value,
        ROUND(SUM(platform_fee), 2) AS platform_revenue,
        ROUND(SUM(provider_payout), 2) AS provider_payout,
        ROUND(AVG(total_amount), 2) AS average_order_value,
        ROUND(SUM(platform_fee) * 100.0 / NULLIF(SUM(total_amount), 0), 2) AS take_rate_pct,
        ROUND(
            SUM(CASE WHEN status IN ('completed', 'approved') THEN 1 ELSE 0 END)
            * 100.0 / NULLIF(COUNT(*), 0),
            2
        ) AS success_rate_pct,
        ROUND(
            SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)
            * 100.0 / NULLIF(COUNT(*), 0),
            2
        ) AS cancellation_rate_pct
    FROM work_orders;
    """
    return read_sql(query)


@st.cache_data(show_spinner=False)
def load_payment_metrics() -> pd.DataFrame:
    query = """
    SELECT
        COUNT(*) AS total_payments,
        SUM(CASE WHEN payment_status = 'late' THEN 1 ELSE 0 END) AS late_payments,
        SUM(CASE WHEN payment_status = 'pending' THEN 1 ELSE 0 END) AS pending_payments,
        ROUND(
            AVG(
                CASE
                    WHEN days_to_pay IS NULL THEN NULL
                    WHEN days_to_pay > 30 THEN days_to_pay - 30
                    ELSE 0
                END
            ),
            2
        ) AS average_payment_delay_days,
        ROUND(
            SUM(CASE WHEN payment_status = 'late' THEN 1 ELSE 0 END)
            * 100.0 / NULLIF(COUNT(*), 0),
            2
        ) AS late_payment_rate_pct
    FROM payments;
    """
    return read_sql(query)


@st.cache_data(show_spinner=False)
def load_monthly_revenue() -> pd.DataFrame:
    query = """
    SELECT
        strftime('%Y-%m', created_at) AS month,
        COUNT(work_order_id) AS total_work_orders,
        SUM(CASE WHEN status IN ('completed', 'approved') THEN 1 ELSE 0 END) AS successful_orders,
        ROUND(SUM(total_amount), 2) AS gross_work_order_value,
        ROUND(SUM(platform_fee), 2) AS platform_revenue,
        ROUND(SUM(provider_payout), 2) AS provider_payout,
        ROUND(AVG(total_amount), 2) AS average_order_value
    FROM work_orders
    GROUP BY strftime('%Y-%m', created_at)
    ORDER BY month;
    """
    return read_sql(query)


@st.cache_data(show_spinner=False)
def load_status_breakdown() -> pd.DataFrame:
    query = """
    SELECT
        status,
        COUNT(*) AS total_work_orders,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS share_of_orders_pct
    FROM work_orders
    GROUP BY status
    ORDER BY total_work_orders DESC;
    """
    return read_sql(query)


@st.cache_data(show_spinner=False)
def load_category_revenue() -> pd.DataFrame:
    query = """
    SELECT
        category,
        COUNT(work_order_id) AS total_work_orders,
        SUM(CASE WHEN status IN ('completed', 'approved') THEN 1 ELSE 0 END) AS successful_orders,
        ROUND(SUM(total_amount), 2) AS gross_work_order_value,
        ROUND(SUM(platform_fee), 2) AS platform_revenue,
        ROUND(AVG(total_amount), 2) AS average_order_value
    FROM work_orders
    GROUP BY category
    ORDER BY gross_work_order_value DESC;
    """
    return read_sql(query)


@st.cache_data(show_spinner=False)
def load_top_buyers() -> pd.DataFrame:
    query = """
    SELECT
        b.company_name,
        b.industry,
        b.buyer_tier,
        b.city,
        b.state,
        COUNT(w.work_order_id) AS total_work_orders,
        ROUND(SUM(w.total_amount), 2) AS gross_work_order_value,
        ROUND(SUM(w.platform_fee), 2) AS platform_revenue,
        ROUND(AVG(w.total_amount), 2) AS average_order_value
    FROM buyers b
    JOIN work_orders w
        ON b.buyer_id = w.buyer_id
    GROUP BY
        b.company_name,
        b.industry,
        b.buyer_tier,
        b.city,
        b.state
    ORDER BY gross_work_order_value DESC
    LIMIT 15;
    """
    return read_sql(query)


@st.cache_data(show_spinner=False)
def load_payment_delay_by_buyer() -> pd.DataFrame:
    query = """
    SELECT
        b.company_name,
        b.industry,
        b.buyer_tier,
        COUNT(p.payment_id) AS total_payments,
        SUM(CASE WHEN p.payment_status = 'late' THEN 1 ELSE 0 END) AS late_payments,
        ROUND(
            AVG(
                CASE
                    WHEN p.days_to_pay IS NULL THEN NULL
                    WHEN p.days_to_pay > 30 THEN p.days_to_pay - 30
                    ELSE 0
                END
            ),
            2
        ) AS average_payment_delay_days,
        ROUND(SUM(p.total_amount), 2) AS payment_value,
        ROUND(SUM(p.platform_fee), 2) AS platform_revenue
    FROM payments p
    JOIN buyers b
        ON p.buyer_id = b.buyer_id
    GROUP BY
        b.company_name,
        b.industry,
        b.buyer_tier
    HAVING COUNT(p.payment_id) >= 3
    ORDER BY average_payment_delay_days DESC, payment_value DESC
    LIMIT 15;
    """
    return read_sql(query)


@st.cache_data(show_spinner=False)
def load_location_performance() -> pd.DataFrame:
    query = """
    SELECT
        city || ', ' || state AS location,
        city,
        state,
        country,
        COUNT(work_order_id) AS total_work_orders,
        SUM(CASE WHEN status IN ('completed', 'approved') THEN 1 ELSE 0 END) AS successful_orders,
        ROUND(SUM(total_amount), 2) AS gross_work_order_value,
        ROUND(SUM(platform_fee), 2) AS platform_revenue,
        ROUND(AVG(total_amount), 2) AS average_order_value
    FROM work_orders
    GROUP BY city, state, country
    ORDER BY gross_work_order_value DESC
    LIMIT 15;
    """
    return read_sql(query)


@st.cache_data(show_spinner=False)
def load_finance_monthly_deep_dive() -> pd.DataFrame:
    return read_sql(read_sql_file("09_finance_monthly_deep_dive.sql"))


@st.cache_data(show_spinner=False)
def load_take_rate_trend() -> pd.DataFrame:
    return read_sql(read_sql_file("10_take_rate_trend.sql"))


@st.cache_data(show_spinner=False)
def load_buyer_revenue_concentration() -> pd.DataFrame:
    return read_sql(read_sql_file("11_buyer_revenue_concentration.sql"))


@st.cache_data(show_spinner=False)
def load_payment_risk_summary() -> pd.DataFrame:
    return read_sql(read_sql_file("12_payment_risk_summary.sql"))


@st.cache_data(show_spinner=False)
def load_category_finance_performance() -> pd.DataFrame:
    return read_sql(read_sql_file("13_category_finance_performance.sql"))


def apply_chart_style(fig):
    """Apply consistent formatting to Plotly charts."""
    fig.update_layout(
        hovermode="x unified",
        legend_title_text="",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


def render_header() -> None:
    st.title("FieldOps Analytics OS")
    st.caption("Executive marketplace finance and field-service operations dashboard")
    st.markdown(
        """
        This dashboard turns synthetic field-service marketplace data into executive-level
        views of revenue, provider payouts, buyer concentration, payment risk, and
        operational health.
        """
    )


def render_kpi_cards() -> None:
    overview = load_overview_metrics().iloc[0]
    payment = load_payment_metrics().iloc[0]

    first_row = st.columns(4)
    first_row[0].metric("Total Work Orders", f"{int(overview['total_work_orders']):,}")
    first_row[1].metric("Gross Work Order Value", format_currency(overview["gross_work_order_value"]))
    first_row[2].metric("Platform Revenue", format_currency(overview["platform_revenue"]))
    first_row[3].metric("Provider Payout", format_currency(overview["provider_payout"]))

    second_row = st.columns(4)
    second_row[0].metric("Take Rate", format_percent(overview["take_rate_pct"]))
    second_row[1].metric("Success Rate", format_percent(overview["success_rate_pct"]))
    second_row[2].metric("Cancellation Rate", format_percent(overview["cancellation_rate_pct"]))
    second_row[3].metric("Average Payment Delay", format_days(payment["average_payment_delay_days"]))


def render_charts() -> None:
    monthly_revenue = load_monthly_revenue()
    status_breakdown = load_status_breakdown()
    category_revenue = load_category_revenue()
    top_buyers = load_top_buyers()
    payment_delay = load_payment_delay_by_buyer()
    location_performance = load_location_performance()

    st.subheader("Revenue Trend")
    revenue_chart = px.line(
        monthly_revenue,
        x="month",
        y=["gross_work_order_value", "platform_revenue", "provider_payout"],
        markers=True,
        title="Monthly Revenue, Fees, and Provider Payouts",
        labels={
            "month": "Month",
            "value": "Amount",
            "variable": "Metric",
        },
    )
    revenue_chart.update_yaxes(tickprefix="$", separatethousands=True)
    st.plotly_chart(apply_chart_style(revenue_chart), use_container_width=True)

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Work Order Status")
        status_chart = px.pie(
            status_breakdown,
            names="status",
            values="total_work_orders",
            title="Work Order Status Breakdown",
            hole=0.45,
        )
        status_chart.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(apply_chart_style(status_chart), use_container_width=True)

    with right_col:
        st.subheader("Revenue by Category")
        category_chart = px.bar(
            category_revenue.sort_values("gross_work_order_value", ascending=False),
            x="category",
            y="gross_work_order_value",
            title="Gross Work Order Value by Category",
            labels={
                "category": "Category",
                "gross_work_order_value": "Gross Work Order Value",
            },
        )
        category_chart.update_yaxes(tickprefix="$", separatethousands=True)
        st.plotly_chart(apply_chart_style(category_chart), use_container_width=True)

    st.subheader("Buyer Concentration")
    buyer_chart = px.bar(
        top_buyers.sort_values("gross_work_order_value"),
        x="gross_work_order_value",
        y="company_name",
        color="industry",
        orientation="h",
        title="Top Buyers by Gross Work Order Value",
        labels={
            "company_name": "Buyer",
            "gross_work_order_value": "Gross Work Order Value",
            "industry": "Industry",
        },
    )
    buyer_chart.update_xaxes(tickprefix="$", separatethousands=True)
    st.plotly_chart(apply_chart_style(buyer_chart), use_container_width=True)

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Payment Delay Risk")
        delay_chart = px.bar(
            payment_delay.sort_values("average_payment_delay_days"),
            x="average_payment_delay_days",
            y="company_name",
            color="buyer_tier",
            orientation="h",
            title="Highest Average Payment Delay by Buyer",
            labels={
                "company_name": "Buyer",
                "average_payment_delay_days": "Average Days After Due Date",
                "buyer_tier": "Buyer Tier",
            },
        )
        st.plotly_chart(apply_chart_style(delay_chart), use_container_width=True)

    with right_col:
        st.subheader("Top Locations")
        location_chart = px.bar(
            location_performance.sort_values("gross_work_order_value"),
            x="gross_work_order_value",
            y="location",
            color="country",
            orientation="h",
            title="Top Locations by Gross Work Order Value",
            labels={
                "location": "Location",
                "gross_work_order_value": "Gross Work Order Value",
                "country": "Country",
            },
        )
        location_chart.update_xaxes(tickprefix="$", separatethousands=True)
        st.plotly_chart(apply_chart_style(location_chart), use_container_width=True)


def render_data_tables() -> None:
    st.subheader("Data Tables")

    tab_names = [
        "Monthly Revenue",
        "Status Breakdown",
        "Category Revenue",
        "Top Buyers",
        "Payment Delay",
        "Locations",
    ]
    tabs = st.tabs(tab_names)

    with tabs[0]:
        st.dataframe(
            load_monthly_revenue(),
            use_container_width=True,
            hide_index=True,
        )

    with tabs[1]:
        st.dataframe(load_status_breakdown(), use_container_width=True, hide_index=True)

    with tabs[2]:
        st.dataframe(
            load_category_revenue(),
            use_container_width=True,
            hide_index=True,
        )

    with tabs[3]:
        st.dataframe(
            load_top_buyers(),
            use_container_width=True,
            hide_index=True,
        )

    with tabs[4]:
        st.dataframe(
            load_payment_delay_by_buyer(),
            use_container_width=True,
            hide_index=True,
        )

    with tabs[5]:
        st.dataframe(
            load_location_performance(),
            use_container_width=True,
            hide_index=True,
        )


def render_business_insights() -> None:
    overview = load_overview_metrics().iloc[0]
    payment = load_payment_metrics().iloc[0]
    category_revenue = load_category_revenue()
    top_buyers = load_top_buyers()
    payment_delay = load_payment_delay_by_buyer()
    location_performance = load_location_performance()

    top_category = category_revenue.iloc[0]
    top_buyer = top_buyers.iloc[0]
    riskiest_buyer = payment_delay.iloc[0]
    top_location = location_performance.iloc[0]

    st.subheader("Business Insights")
    st.markdown(
        f"""
        **Marketplace scale:** The platform processed **{int(overview['total_work_orders']):,} work orders**
        and generated **{format_currency(overview['gross_work_order_value'])}** in gross work order value.
        At a **{format_percent(overview['take_rate_pct'])}** take rate, this produced
        **{format_currency(overview['platform_revenue'])}** in platform revenue while passing
        **{format_currency(overview['provider_payout'])}** through to providers.

        **Operational health:** The current success rate is
        **{format_percent(overview['success_rate_pct'])}**, compared with a cancellation rate of
        **{format_percent(overview['cancellation_rate_pct'])}**. This suggests the marketplace is
        converting most created work orders into completed or approved jobs, while cancellations remain
        a meaningful area to monitor.

        **Revenue mix:** **{top_category['category']}** is the largest category by gross work order
        value, contributing **{format_currency(top_category['gross_work_order_value'])}**. This category
        is a good candidate for deeper analysis of provider supply, pricing, and repeat buyer demand.

        **Buyer concentration:** The highest-value buyer is **{top_buyer['company_name']}**, representing
        **{format_currency(top_buyer['gross_work_order_value'])}** in gross value. Executive reporting
        should watch whether growth is broad-based or overly dependent on a small group of buyers.

        **Payment risk:** Average payment delay is **{format_days(payment['average_payment_delay_days'])}**
        after the due date across settled payments. **{riskiest_buyer['company_name']}** has the highest
        average delay among buyers with at least three payments, making it a logical candidate for credit
        or collections review.

        **Market footprint:** **{top_location['location']}** is the strongest location by gross work order
        value at **{format_currency(top_location['gross_work_order_value'])}**. High-performing locations
        can guide provider recruiting, sales coverage, and category expansion priorities.
        """
    )


def render_finance_deep_dive() -> None:
    monthly_finance = load_finance_monthly_deep_dive()
    take_rate_trend = load_take_rate_trend()
    buyer_concentration = load_buyer_revenue_concentration()
    payment_risk = load_payment_risk_summary()
    category_finance = load_category_finance_performance()

    if (
        monthly_finance.empty
        or buyer_concentration.empty
        or payment_risk.empty
        or category_finance.empty
    ):
        st.warning("Finance deep dive data is not available yet.")
        return

    latest_month = monthly_finance.iloc[-1]
    previous_month = monthly_finance.iloc[-2] if len(monthly_finance) > 1 else None
    top_buyer = buyer_concentration.iloc[0]
    top_category = category_finance.iloc[0]
    riskiest_buyer = payment_risk.iloc[0]

    if previous_month is not None and previous_month["platform_revenue"] != 0:
        platform_revenue_change = (
            (latest_month["platform_revenue"] - previous_month["platform_revenue"])
            * 100.0
            / previous_month["platform_revenue"]
        )
        platform_revenue_trend = f"{platform_revenue_change:+.1f}% month over month"
    else:
        platform_revenue_trend = "not enough month history"

    top_5_share = buyer_concentration.head(5)["revenue_share_pct"].sum()
    top_10_share = buyer_concentration.head(10)["revenue_share_pct"].sum()
    high_risk_buyers = payment_risk[payment_risk["payment_risk_level"] == "High Risk"]

    st.header("Finance Analytics Deep Dive")
    st.caption("v0.5 finance view for revenue quality, monetization, concentration, and payment risk")

    kpi_cols = st.columns(4)
    kpi_cols[0].metric(
        "Latest Platform Revenue",
        format_currency(latest_month["platform_revenue"]),
        platform_revenue_trend,
    )
    kpi_cols[1].metric("Latest Take Rate", format_percent(latest_month["take_rate_pct"]))
    kpi_cols[2].metric("Top 5 Buyer Share", format_percent(top_5_share))
    kpi_cols[3].metric("High Risk Buyers", f"{len(high_risk_buyers):,}")

    concentration_cols = st.columns(4)
    concentration_cols[0].metric("Largest Buyer Share", format_percent(top_buyer["revenue_share_pct"]))
    concentration_cols[1].metric("Top 10 Buyer Share", format_percent(top_10_share))
    concentration_cols[2].metric("Top Buyer Revenue", format_currency(top_buyer["platform_revenue"]))
    concentration_cols[3].metric(
        "Avg Payment Delay",
        format_days(payment_risk["average_payment_delay_days"].mean()),
    )

    st.subheader("Monthly Finance Performance")
    finance_chart = px.line(
        monthly_finance,
        x="month",
        y=["gross_work_order_value", "platform_revenue", "provider_payout"],
        markers=True,
        title="Monthly Gross Work Order Value, Platform Revenue, and Provider Payout",
        labels={
            "month": "Month",
            "value": "Amount",
            "variable": "Metric",
        },
    )
    finance_chart.update_yaxes(tickprefix="$", separatethousands=True)
    st.plotly_chart(apply_chart_style(finance_chart), use_container_width=True)

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Take Rate Trend")
        take_rate_chart = px.line(
            take_rate_trend,
            x="month",
            y="take_rate_pct",
            color="category",
            markers=True,
            title="Monthly Take Rate by Category",
            labels={
                "month": "Month",
                "take_rate_pct": "Take Rate",
                "category": "Category",
            },
        )
        take_rate_chart.update_yaxes(ticksuffix="%")
        st.plotly_chart(apply_chart_style(take_rate_chart), use_container_width=True)

    with right_col:
        st.subheader("Average Work Order Value")
        aov_chart = px.line(
            monthly_finance,
            x="month",
            y="average_work_order_value",
            markers=True,
            title="Monthly Average Work Order Value",
            labels={
                "month": "Month",
                "average_work_order_value": "Average Work Order Value",
            },
        )
        aov_chart.update_yaxes(tickprefix="$", separatethousands=True)
        st.plotly_chart(apply_chart_style(aov_chart), use_container_width=True)

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Top Buyers by Platform Revenue")
        buyer_chart = px.bar(
            buyer_concentration.head(10).sort_values("platform_revenue"),
            x="platform_revenue",
            y="company_name",
            color="industry",
            orientation="h",
            title="Top 10 Buyers by Platform Revenue",
            labels={
                "platform_revenue": "Platform Revenue",
                "company_name": "Buyer",
                "industry": "Industry",
            },
        )
        buyer_chart.update_xaxes(tickprefix="$", separatethousands=True)
        st.plotly_chart(apply_chart_style(buyer_chart), use_container_width=True)

    with right_col:
        st.subheader("Category Finance Performance")
        category_chart = px.bar(
            category_finance.sort_values("platform_revenue", ascending=False),
            x="category",
            y="platform_revenue",
            color="take_rate_pct",
            title="Platform Revenue by Category",
            labels={
                "category": "Category",
                "platform_revenue": "Platform Revenue",
                "take_rate_pct": "Take Rate",
            },
        )
        category_chart.update_yaxes(tickprefix="$", separatethousands=True)
        st.plotly_chart(apply_chart_style(category_chart), use_container_width=True)

    st.subheader("Payment Delay Risk")
    payment_chart = px.bar(
        payment_risk.head(15).sort_values("average_payment_delay_days"),
        x="average_payment_delay_days",
        y="company_name",
        color="payment_risk_level",
        orientation="h",
        title="Payment Delay Risk by Buyer",
        labels={
            "average_payment_delay_days": "Average Days After Due Date",
            "company_name": "Buyer",
            "payment_risk_level": "Risk Level",
        },
    )
    st.plotly_chart(apply_chart_style(payment_chart), use_container_width=True)

    st.subheader("Finance Analyst Notes")
    st.markdown(
        f"""
        **Revenue quality:** Latest month platform revenue was
        **{format_currency(latest_month['platform_revenue'])}**, with a
        **{format_percent(latest_month['take_rate_pct'])}** take rate. The month-over-month platform
        revenue trend is **{platform_revenue_trend}**, which should be reviewed alongside gross work
        order value to separate pricing changes from true marketplace growth.

        **Buyer concentration:** **{top_buyer['company_name']}** is the largest buyer by platform
        revenue and represents **{format_percent(top_buyer['revenue_share_pct'])}** of total platform
        revenue. The top 5 buyers represent **{format_percent(top_5_share)}**, so account health and
        renewal risk should be part of the monthly finance review.

        **Category mix:** **{top_category['category']}** is the leading category by platform revenue at
        **{format_currency(top_category['platform_revenue'])}**. Its take rate is
        **{format_percent(top_category['take_rate_pct'])}**, making it a useful benchmark for pricing
        and service-line expansion.

        **Collections risk:** **{riskiest_buyer['company_name']}** has the highest average payment
        delay among buyers with at least three payments. This buyer combines
        **{format_currency(riskiest_buyer['platform_revenue'])}** in platform revenue with a
        **{format_percent(riskiest_buyer['late_payment_rate_pct'])}** late payment rate, making it a
        priority for credit or collections follow-up.
        """
    )

    st.subheader("Finance Data Tables")
    tabs = st.tabs(
        [
            "Monthly Finance",
            "Take Rate Trend",
            "Buyer Concentration",
            "Payment Risk",
            "Category Finance",
        ]
    )

    with tabs[0]:
        st.dataframe(monthly_finance, use_container_width=True, hide_index=True)

    with tabs[1]:
        st.dataframe(take_rate_trend, use_container_width=True, hide_index=True)

    with tabs[2]:
        st.dataframe(buyer_concentration, use_container_width=True, hide_index=True)

    with tabs[3]:
        st.dataframe(payment_risk, use_container_width=True, hide_index=True)

    with tabs[4]:
        st.dataframe(category_finance, use_container_width=True, hide_index=True)


def main() -> None:
    validate_database()
    render_header()

    st.divider()
    render_kpi_cards()

    st.divider()
    render_charts()

    st.divider()
    render_data_tables()

    st.divider()
    render_business_insights()

    st.divider()
    render_finance_deep_dive()


if __name__ == "__main__":
    main()
