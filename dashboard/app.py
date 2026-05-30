"""
Streamlit Executive Dashboard for FieldOps Analytics OS.

This dashboard reads from:
- data/processed/fieldops.db

Run:
streamlit run dashboard/app.py
"""

from pathlib import Path
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "processed" / "fieldops.db"
SQL_DIR = PROJECT_ROOT / "sql"

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


def format_filter_label(value: str) -> str:
    """Make database values easier to scan in filter controls."""
    return value.replace("_", " ").title()


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
def load_dashboard_dataset() -> pd.DataFrame:
    """Load the joined work order, buyer, and payment dataset for filters."""
    query = """
    SELECT
        w.work_order_id,
        w.buyer_id,
        w.provider_id,
        w.category AS service_category,
        w.work_order_title,
        w.city,
        w.state,
        w.country,
        w.priority,
        w.status,
        w.created_at,
        w.assigned_at,
        w.completed_at,
        w.approved_at,
        w.total_amount AS gross_work_order_value,
        w.platform_fee AS platform_revenue,
        w.provider_payout,
        w.take_rate,
        w.is_emergency,
        b.company_name,
        b.industry AS buyer_industry,
        b.buyer_tier,
        b.city AS buyer_city,
        b.state AS buyer_state,
        b.country AS buyer_country,
        p.payment_id,
        p.payment_status,
        p.payment_method,
        p.payment_due_date,
        p.paid_at,
        p.days_to_pay,
        p.is_late
    FROM work_orders w
    LEFT JOIN buyers b
        ON w.buyer_id = b.buyer_id
    LEFT JOIN payments p
        ON w.work_order_id = p.work_order_id;
    """
    dashboard_df = read_sql(query)

    date_columns = [
        "created_at",
        "assigned_at",
        "completed_at",
        "approved_at",
        "payment_due_date",
        "paid_at",
    ]
    for column in date_columns:
        dashboard_df[column] = pd.to_datetime(dashboard_df[column], errors="coerce")

    money_columns = [
        "gross_work_order_value",
        "platform_revenue",
        "provider_payout",
        "take_rate",
        "days_to_pay",
    ]
    for column in money_columns:
        dashboard_df[column] = pd.to_numeric(dashboard_df[column], errors="coerce")

    dashboard_df["payment_delay_days"] = (
        dashboard_df["days_to_pay"].sub(30).clip(lower=0)
    )
    dashboard_df["created_month"] = dashboard_df["created_at"].dt.to_period("M").astype(str)

    return dashboard_df


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


def get_filter_options(df: pd.DataFrame, column: str) -> list[str]:
    """Return sorted, non-empty values for sidebar filters."""
    values = df[column].dropna().astype(str)
    return sorted(value for value in values.unique() if value.strip())


def apply_dashboard_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply sidebar filters to the joined dashboard dataset."""
    st.sidebar.header("Dashboard Filters")
    st.sidebar.caption("Filters apply to the interactive section at the top.")

    min_ts = df["created_at"].min()
    max_ts = df["created_at"].max()
    selected_date_range = None
    if pd.notna(min_ts) and pd.notna(max_ts):
        min_date = min_ts.date()
        max_date = max_ts.date()
        selected_date_range = st.sidebar.date_input(
            "Created date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

    category_options = get_filter_options(df, "service_category")
    status_options = get_filter_options(df, "status")
    industry_options = get_filter_options(df, "buyer_industry")
    country_options = get_filter_options(df, "country")

    selected_categories = st.sidebar.multiselect(
        "Service category",
        options=category_options,
        default=category_options,
    )
    selected_statuses = st.sidebar.multiselect(
        "Work order status",
        options=status_options,
        default=status_options,
        format_func=format_filter_label,
    )
    selected_industries = st.sidebar.multiselect(
        "Buyer industry",
        options=industry_options,
        default=industry_options,
    )
    selected_countries = st.sidebar.multiselect(
        "Country",
        options=country_options,
        default=country_options,
    )

    filtered_df = df.copy()

    if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
        filtered_df = filtered_df[
            (filtered_df["created_at"].dt.date >= start_date)
            & (filtered_df["created_at"].dt.date <= end_date)
        ]

    filtered_df = filtered_df[
        filtered_df["service_category"].isin(selected_categories)
        & filtered_df["status"].isin(selected_statuses)
        & filtered_df["buyer_industry"].isin(selected_industries)
        & filtered_df["country"].isin(selected_countries)
    ]

    return filtered_df


def calculate_filtered_metrics(df: pd.DataFrame) -> dict[str, float]:
    """Calculate KPI values for the filtered dashboard section."""
    total_orders = len(df)
    gross_value = df["gross_work_order_value"].sum()
    platform_revenue = df["platform_revenue"].sum()
    provider_payout = df["provider_payout"].sum()
    successful_orders = df["status"].isin(["completed", "approved"]).sum()
    cancelled_orders = (df["status"] == "cancelled").sum()

    take_rate = platform_revenue * 100.0 / gross_value if gross_value else 0
    success_rate = successful_orders * 100.0 / total_orders if total_orders else 0
    cancellation_rate = cancelled_orders * 100.0 / total_orders if total_orders else 0
    average_delay = df["payment_delay_days"].mean()

    return {
        "total_orders": total_orders,
        "gross_value": gross_value,
        "platform_revenue": platform_revenue,
        "provider_payout": provider_payout,
        "take_rate": take_rate,
        "success_rate": success_rate,
        "cancellation_rate": cancellation_rate,
        "average_delay": average_delay,
    }


def render_filtered_kpi_cards(df: pd.DataFrame) -> None:
    """Render KPI cards for the active filter selection."""
    metrics = calculate_filtered_metrics(df)

    first_row = st.columns(4)
    first_row[0].metric("Filtered Work Orders", f"{metrics['total_orders']:,.0f}")
    first_row[1].metric("Gross Work Order Value", format_currency(metrics["gross_value"]))
    first_row[2].metric("Platform Revenue", format_currency(metrics["platform_revenue"]))
    first_row[3].metric("Provider Payout", format_currency(metrics["provider_payout"]))

    second_row = st.columns(4)
    second_row[0].metric("Take Rate", format_percent(metrics["take_rate"]))
    second_row[1].metric("Success Rate", format_percent(metrics["success_rate"]))
    second_row[2].metric("Cancellation Rate", format_percent(metrics["cancellation_rate"]))
    second_row[3].metric("Average Payment Delay", format_days(metrics["average_delay"]))


def render_filtered_charts(df: pd.DataFrame) -> None:
    """Render charts that respond to the sidebar filters."""
    monthly_revenue = (
        df.groupby("created_month", as_index=False)
        .agg(
            gross_work_order_value=("gross_work_order_value", "sum"),
            platform_revenue=("platform_revenue", "sum"),
            provider_payout=("provider_payout", "sum"),
        )
        .sort_values("created_month")
    )
    status_breakdown = (
        df.groupby("status", as_index=False)
        .agg(total_work_orders=("work_order_id", "count"))
        .sort_values("total_work_orders", ascending=False)
    )
    category_revenue = (
        df.groupby("service_category", as_index=False)
        .agg(platform_revenue=("platform_revenue", "sum"))
        .sort_values("platform_revenue", ascending=False)
    )
    top_buyers = (
        df.groupby(["company_name", "buyer_industry"], as_index=False)
        .agg(platform_revenue=("platform_revenue", "sum"))
        .sort_values("platform_revenue", ascending=False)
        .head(10)
    )

    st.subheader("Filtered Monthly Revenue Trend")
    revenue_chart = px.line(
        monthly_revenue,
        x="created_month",
        y=["gross_work_order_value", "platform_revenue", "provider_payout"],
        markers=True,
        title="Monthly Gross Value, Platform Revenue, and Provider Payout",
        labels={
            "created_month": "Created Month",
            "value": "Amount",
            "variable": "Metric",
        },
    )
    revenue_chart.update_yaxes(tickprefix="$", separatethousands=True)
    st.plotly_chart(apply_chart_style(revenue_chart), use_container_width=True)

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Filtered Status Breakdown")
        status_chart = px.pie(
            status_breakdown,
            names="status",
            values="total_work_orders",
            title="Work Orders by Status",
            hole=0.45,
        )
        status_chart.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(apply_chart_style(status_chart), use_container_width=True)

    with right_col:
        st.subheader("Filtered Platform Revenue by Category")
        category_chart = px.bar(
            category_revenue,
            x="service_category",
            y="platform_revenue",
            title="Platform Revenue by Service Category",
            labels={
                "service_category": "Service Category",
                "platform_revenue": "Platform Revenue",
            },
        )
        category_chart.update_yaxes(tickprefix="$", separatethousands=True)
        st.plotly_chart(apply_chart_style(category_chart), use_container_width=True)

    st.subheader("Filtered Top Buyers")
    buyer_chart = px.bar(
        top_buyers.sort_values("platform_revenue"),
        x="platform_revenue",
        y="company_name",
        color="buyer_industry",
        orientation="h",
        title="Top 10 Buyers by Platform Revenue",
        labels={
            "platform_revenue": "Platform Revenue",
            "company_name": "Buyer",
            "buyer_industry": "Buyer Industry",
        },
    )
    buyer_chart.update_xaxes(tickprefix="$", separatethousands=True)
    st.plotly_chart(apply_chart_style(buyer_chart), use_container_width=True)


def render_metric_glossary() -> None:
    """Show short business definitions for dashboard metrics."""
    with st.expander("Metric Glossary"):
        st.markdown(
            """
            **Filtered Work Orders:** Count of work orders after sidebar filters are applied.

            **Gross Work Order Value:** Total work order value before platform fees and provider payouts.

            **Platform Revenue:** Fees retained by the marketplace.

            **Provider Payout:** Amount passed through to service providers.

            **Take Rate:** Platform revenue divided by gross work order value.

            **Success Rate:** Share of filtered work orders with completed or approved status.

            **Cancellation Rate:** Share of filtered work orders with cancelled status.

            **Average Payment Delay:** Average days paid after the 30-day due window for settled payments.
            """
        )


def render_csv_export(df: pd.DataFrame) -> None:
    """Provide a CSV export for the current filtered dataset."""
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered dataset as CSV",
        data=csv_data,
        file_name="fieldops_filtered_dashboard_dataset.csv",
        mime="text/csv",
    )


def render_interactive_dashboard() -> None:
    """Render the v0.7 interactive, filterable dashboard section."""
    dashboard_df = load_dashboard_dataset()
    filtered_df = apply_dashboard_filters(dashboard_df)

    st.header("Interactive Dashboard")
    st.caption("v0.7 filtered marketplace finance and work-order analytics")

    if filtered_df.empty:
        st.warning("No work orders match the current filters. Adjust the sidebar filters to continue.")
        return

    render_filtered_kpi_cards(filtered_df)
    render_filtered_charts(filtered_df)
    render_csv_export(filtered_df)
    render_metric_glossary()


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

    st.subheader("Business Insights")

    # payment_delay applies HAVING COUNT(*) >= 3, so it can be empty on small
    # datasets even when the other tables have rows. Guard before .iloc[0].
    if (
        category_revenue.empty
        or top_buyers.empty
        or payment_delay.empty
        or location_performance.empty
    ):
        st.info("Not enough data yet to generate written business insights.")
        return

    top_category = category_revenue.iloc[0]
    top_buyer = top_buyers.iloc[0]
    riskiest_buyer = payment_delay.iloc[0]
    top_location = location_performance.iloc[0]
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
    render_interactive_dashboard()

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
