# FieldOps Analytics OS

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b)](https://streamlit.io/)
[![SQLite](https://img.shields.io/badge/SQLite-Analytics%20DB-003b57)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Marketplace Finance, Operations, and Business Intelligence Case Study**

[Open the Live Dashboard](https://fieldops-analytics-os.streamlit.app/)

FieldOps Analytics OS is a portfolio-ready analytics project that simulates a field-service marketplace, builds a local SQLite analytics database, runs a library of SQL analysis queries, and presents executive insights in a Streamlit dashboard.

**Live App:** https://fieldops-analytics-os.streamlit.app/

The project is designed for **Data Analyst**, **Business Intelligence Analyst**, **Finance Analyst**, and **Marketplace Operations Analyst** roles. It demonstrates end-to-end analytical thinking: dataset design, data pipeline execution, SQL analysis, KPI development, dashboard storytelling, and business recommendation writing.

## Live Demo

[Open the Live Dashboard](https://fieldops-analytics-os.streamlit.app/)

## Business Problem

Field-service marketplaces need to balance growth, revenue quality, provider payouts, buyer concentration, and payment risk. Leadership needs clear answers to questions such as:

- How much marketplace volume is being generated?
- How much platform revenue is retained after provider payouts?
- Is the marketplace take rate stable over time and across categories?
- Which buyers and service categories drive the most financial value?
- Is revenue overly concentrated in a small number of buyer accounts?
- Which buyers create late-payment or collections risk?
- Are work orders being completed successfully, or are cancellations rising?

## Project Objective

Build a complete business intelligence workflow that turns synthetic marketplace transactions into decision-ready reporting:

- Generate realistic synthetic marketplace data.
- Load the data into a relational SQLite database.
- Run reusable SQL analysis files.
- Export query outputs for reporting and review.
- Build an interactive Streamlit executive dashboard.
- Document the business case, data model, SQL layer, dashboard, and insights.

## Dashboard Preview

Add the following screenshots after running the dashboard locally:

### Interactive Dashboard

![Interactive Dashboard](assets/screenshots/interactive-dashboard.png)

### Executive Dashboard

![Executive Dashboard](assets/screenshots/executive-dashboard.png)

### Finance Analytics Deep Dive

![Finance Deep Dive](assets/screenshots/finance-deep-dive.png)

### Buyer Revenue Concentration

![Buyer Concentration](assets/screenshots/buyer-concentration.png)

### Payment Risk Analysis

![Payment Risk](assets/screenshots/payment-risk.png)

## Tech Stack

| Layer | Tools |
| --- | --- |
| Programming | Python |
| Data generation | Faker, NumPy, pandas |
| Data storage | SQLite |
| Analysis | SQL, pandas |
| Dashboard | Streamlit |
| Visualization | Plotly |
| Documentation | Markdown |
| Version control | Git, GitHub |

## Architecture

```text
fieldops-analytics-os/
|-- dashboard/
|   `-- app.py
|-- .streamlit/
|   `-- config.toml
|-- data/
|   |-- raw/
|   `-- processed/
|-- docs/
|   |-- case_study.md
|   |-- data_model.md
|   |-- sql_analysis_guide.md
|   |-- dashboard_guide.md
|   |-- dashboard_ux_notes.md
|   |-- business_insights.md
|   |-- portfolio_summary.md
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
|   |-- __init__.py
|   |-- bootstrap_data.py
|   |-- generate_data.py
|   |-- load_to_sqlite.py
|   `-- run_sql_queries.py
|-- LICENSE
|-- README.md
`-- requirements.txt
```

## Dataset Design

The project uses a synthetic relational dataset for a two-sided field-service marketplace.

| Table | Purpose |
| --- | --- |
| `buyers` | Companies purchasing field-service work. |
| `providers` | Service providers completing work orders. |
| `work_orders` | Core marketplace transactions, including category, status, amount, fee, payout, and take rate. |
| `payments` | Payment status, due dates, paid dates, delays, and payment value. |
| `reviews` | Buyer feedback and rehire intent for completed work. |
| `support_tickets` | Operational support issues linked to buyers and work orders. |

The seeded sample dataset generates:

- 500 buyers
- 1,500 providers
- 10,000 work orders
- Payment records for completed or approved work orders
- Reviews and support tickets for operational context

## KPI List

| KPI | Business meaning |
| --- | --- |
| Gross Work Order Value | Total marketplace transaction value before fees and payouts. |
| Platform Revenue | Revenue retained by the marketplace through platform fees. |
| Provider Payout | Amount paid out to service providers. |
| Take Rate | Platform revenue divided by gross work order value. |
| Average Work Order Value | Average dollar value per work order. |
| Success Rate | Share of work orders completed or approved. |
| Cancellation Rate | Share of work orders cancelled. |
| Buyer Revenue Share | Share of platform revenue generated by each buyer. |
| Late Payment Rate | Share of payments marked late. |
| Average Payment Delay | Average days paid after the due date. |

## SQL Analysis Library

| File | Analysis |
| --- | --- |
| `sql/01_revenue_kpis.sql` | Monthly revenue, platform fees, payouts, AOV, and take rate. |
| `sql/02_work_order_health.sql` | Completion, approval, cancellation, pending, and assignment status health. |
| `sql/03_top_buyers.sql` | Top buyer accounts by gross value and platform revenue. |
| `sql/04_provider_performance.sql` | Provider workload, payout, completion, cancellation, and rating performance. |
| `sql/05_category_revenue.sql` | Revenue and payout performance by service category. |
| `sql/06_location_performance.sql` | Marketplace performance by city, state, and country. |
| `sql/07_payment_delay.sql` | Buyer-level payment status and late-payment analysis. |
| `sql/08_marketplace_health.sql` | Monthly health view combining work orders, payments, reviews, and support tickets. |
| `sql/09_finance_monthly_deep_dive.sql` | Monthly finance performance and take rate analysis. |
| `sql/10_take_rate_trend.sql` | Take rate trend by month and category. |
| `sql/11_buyer_revenue_concentration.sql` | Buyer concentration and revenue share ranking. |
| `sql/12_payment_risk_summary.sql` | Buyer payment risk levels using delay and late-payment metrics. |
| `sql/13_category_finance_performance.sql` | Category-level finance performance, payout rate, AOV, and success rate. |

## Dashboard Sections

The Streamlit dashboard includes:

- Interactive filtered dashboard section with sidebar filters for created date range, service category, work order status, buyer industry, and country.
- Filtered KPI cards for work orders, gross value, platform revenue, payout, take rate, success rate, cancellation rate, and payment delay.
- Filtered charts for monthly revenue trend, status breakdown, platform revenue by category, and top buyers by platform revenue.
- CSV export for the active filtered dataset.
- Metric glossary explaining KPI definitions.
- Executive KPI cards for work orders, gross value, platform revenue, payout, take rate, success rate, cancellation rate, and payment delay.
- Monthly revenue trend for gross work order value, platform revenue, and provider payout.
- Work order status breakdown.
- Revenue by service category.
- Buyer concentration chart.
- Payment delay risk chart.
- Top location performance.
- Interactive data tables.
- Business insights narrative.
- Finance deep dive for monthly finance performance, take rate trends, buyer concentration, payment risk, and category finance performance.

## Example Business Insights

Using the current seeded sample output:

- The marketplace processed 10,000 work orders.
- Gross work order value is approximately $13.3M.
- Platform revenue is approximately $2.3M, with an overall take rate near 17%.
- Provider payout is approximately $11.1M.
- Work order success rate is 62.45%, while cancellation rate is 8.79%.
- Roofing is the highest platform revenue category in the current sample.
- Buyer concentration is distributed across many accounts, with the largest buyer under 1% of platform revenue.
- Several buyers show high payment-delay risk and should be reviewed for credit or collections follow-up.

Because the data is synthetic and generated with a fixed seed, these insights are reproducible unless the generator assumptions are changed.

## Documentation

| Document | Purpose |
| --- | --- |
| [Case Study](docs/case_study.md) | Business problem, objective, approach, deliverables, and role alignment. |
| [Data Model](docs/data_model.md) | Table design, relationships, and analytical grain. |
| [SQL Analysis Guide](docs/sql_analysis_guide.md) | Query library and business questions answered by each SQL file. |
| [Dashboard Guide](docs/dashboard_guide.md) | Dashboard sections, screenshot plan, and user workflow. |
| [Dashboard UX Notes](docs/dashboard_ux_notes.md) | v0.7 filter, export, glossary, and screenshot notes. |
| [Business Insights](docs/business_insights.md) | KPI interpretation, findings, recommendations, and analyst talking points. |
| [Project Architecture](docs/project_architecture.md) | Pipeline flow, folder structure, and execution sequence. |
| [Portfolio Summary](docs/portfolio_summary.md) | Concise portfolio positioning, skills demonstrated, KPIs, and target roles. |

## How to Run Locally

1. Clone the repository and open the project folder.

2. Create and activate a virtual environment.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies.

```bash
pip install -r requirements.txt
```

4. Generate synthetic data.

```bash
python src/generate_data.py
```

5. Load data into SQLite.

```bash
python src/load_to_sqlite.py
```

6. Run SQL analyses and export CSV outputs.

```bash
python src/run_sql_queries.py
```

7. Launch the Streamlit dashboard.

```bash
streamlit run dashboard/app.py
```

The dashboard also includes a deployment bootstrap. If `data/processed/fieldops.db` is missing, it automatically runs:

```bash
python src/generate_data.py
python src/load_to_sqlite.py
```

Generated CSV files and SQLite databases are intentionally ignored by Git because the project uses reproducible synthetic data.

## Streamlit Community Cloud Deployment

1. Push this repository to GitHub without generated CSV files or SQLite databases.
2. Open [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Create a new app from the GitHub repository.
4. Set the main file path to:

```text
dashboard/app.py
```

5. Confirm the dependency file is:

```text
requirements.txt
```

6. Deploy the app. No secrets are required because all data is synthetic and generated by the app bootstrap when the SQLite database is missing.

The live Streamlit dashboard is available at:

[Open the Live Dashboard](https://fieldops-analytics-os.streamlit.app/)

## Final Portfolio Summary

FieldOps Analytics OS is a complete analytics portfolio case study for a synthetic field-service marketplace. It demonstrates how to design data, build a repeatable Python-to-SQLite pipeline, write reusable SQL analysis, create executive dashboard views, and translate metrics into business recommendations.

The project is positioned for analyst roles that require both technical execution and business communication: data analytics, business intelligence, finance analytics, marketplace operations, and revenue operations.

## Version Roadmap

| Version | Focus |
| --- | --- |
| v0.1 | Project setup and initial folder structure. |
| v0.2 | Synthetic marketplace data generation. |
| v0.3 | SQLite loading and relational analytics database. |
| v0.4 | SQL analysis library and exported query outputs. |
| v0.5 | Streamlit dashboard and finance analytics deep dive. |
| v0.6 | Business intelligence case study and documentation upgrade. |
| v0.7 | Dashboard UX, sidebar filters, CSV export, metric glossary, and portfolio polish |
| v0.8 | Deployment and final GitHub portfolio packaging. |
| v1.0 | Portfolio-ready release with complete visuals, documentation, and live demo URL. |

## v0.7 Notes

v0.7 adds an interactive dashboard section near the top of the Streamlit app. It joins `work_orders`, `buyers`, and `payments` from SQLite, lets the viewer filter the dataset from the sidebar, refreshes KPI cards and charts based on the active selection, and exports the filtered rows as CSV.

## Portfolio Value

This project shows the ability to:

- Design a realistic business analytics dataset.
- Build a repeatable Python-to-SQLite pipeline.
- Write business-focused SQL queries.
- Translate metrics into executive-ready dashboard views.
- Analyze marketplace revenue quality, concentration risk, payment risk, and operations health.
- Communicate findings clearly for business stakeholders.

