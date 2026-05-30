# Project Architecture

FieldOps Analytics OS is built as a local analytics pipeline with a Streamlit dashboard on top of a SQLite database.

## Architecture Flow

```text
src/generate_data.py
        |
        v
data/raw/*.csv
        |
        v
src/load_to_sqlite.py
        |
        v
data/processed/fieldops.db
        |
        v
sql/*.sql
        |
        v
src/run_sql_queries.py
        |
        v
reports/query_outputs/*.csv
        |
        v
dashboard/app.py
        |
        v
Streamlit dashboard
```

## Component Responsibilities

| Component | Responsibility |
| --- | --- |
| `src/generate_data.py` | Generates synthetic buyers, providers, work orders, payments, reviews, and support tickets. |
| `data/raw/` | Stores generated CSV files. |
| `src/load_to_sqlite.py` | Validates raw files, rebuilds the SQLite database, loads tables, and creates indexes. |
| `data/processed/fieldops.db` | Stores the local analytics database. |
| `sql/` | Stores reusable SQLite analysis queries. |
| `src/run_sql_queries.py` | Executes every SQL file and exports outputs to CSV. |
| `reports/query_outputs/` | Stores query result exports for review and reporting. |
| `dashboard/app.py` | Runs the Streamlit dashboard and reads directly from SQLite. |
| `docs/` | Stores case study, data model, SQL, dashboard, business insights, and architecture documentation. |
| `assets/screenshots/` | Stores dashboard screenshots used in the README. |

## Folder Structure

```text
fieldops-analytics-os/
|-- assets/
|   `-- screenshots/
|       |-- executive-dashboard.png
|       |-- finance-deep-dive.png
|       |-- buyer-concentration.png
|       `-- payment-risk.png
|-- dashboard/
|   `-- app.py
|-- data/
|   |-- raw/
|   `-- processed/
|-- docs/
|   |-- case_study.md
|   |-- data_model.md
|   |-- sql_analysis_guide.md
|   |-- dashboard_guide.md
|   |-- business_insights.md
|   `-- project_architecture.md
|-- reports/
|   |-- finance_insights.md
|   `-- query_outputs/
|-- sql/
|   |-- 01_revenue_kpis.sql
|   |-- 02_work_order_health.sql
|   |-- 03_top_buyers.sql
|   |-- 04_provider_performance.sql
|   |-- 05_category_revenue.sql
|   |-- 06_location_performance.sql
|   |-- 07_payment_delay.sql
|   |-- 08_marketplace_health.sql
|   |-- 09_finance_monthly_deep_dive.sql
|   |-- 10_take_rate_trend.sql
|   |-- 11_buyer_revenue_concentration.sql
|   |-- 12_payment_risk_summary.sql
|   `-- 13_category_finance_performance.sql
|-- src/
|   |-- generate_data.py
|   |-- load_to_sqlite.py
|   `-- run_sql_queries.py
|-- README.md
`-- requirements.txt
```

## Execution Sequence

1. Generate synthetic data.

```bash
python src/generate_data.py
```

2. Load the SQLite database.

```bash
python src/load_to_sqlite.py
```

3. Run SQL analyses.

```bash
python src/run_sql_queries.py
```

4. Launch the dashboard.

```bash
streamlit run dashboard/app.py
```

## Data Flow

The data generator creates raw CSV files. The loader imports those files into SQLite and creates indexes for common analytical paths. SQL files provide reproducible analysis outputs, while the Streamlit dashboard reads from the database and selected SQL files to display executive and finance views.

## Design Principles

- Keep the pipeline simple enough to run locally.
- Use SQL for transparent and reviewable business logic.
- Keep dashboard logic focused on presentation and lightweight transformations.
- Separate documentation by audience: case study, data model, SQL guide, dashboard guide, insights, and architecture.
- Make the project easy to evaluate in a GitHub portfolio review.

