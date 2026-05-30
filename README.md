# FieldOps Analytics OS

FieldOps Analytics OS is a marketplace finance and work-order analytics project inspired by field-service platforms. It analyzes synthetic work-order data to track revenue, provider payouts, buyer activity, payment delays, marketplace health, and operational performance.

## Project Goal

The goal of this project is to simulate the kind of analytics work performed by data analysts, business intelligence analysts, and finance analytics teams inside marketplace companies.

This project focuses on:

- Work order analytics
- Revenue and finance KPIs
- Provider payout analysis
- Buyer/customer performance
- Payment delay tracking
- Marketplace health metrics
- SQL-based business analysis
- Interactive dashboard development

## Business Context

A field-service marketplace connects companies that need on-site work with technicians or service providers who complete those jobs.

Examples of marketplace questions this project answers:

- How much revenue is the marketplace generating?
- Which work categories create the most revenue?
- Which buyers spend the most?
- Which providers complete the most jobs?
- What percentage of work orders are completed, cancelled, or delayed?
- How long does it take for payments to be completed?
- Which locations have strong or weak marketplace performance?

## Planned Tech Stack

- Python
- Pandas
- NumPy
- Faker
- SQL
- SQLite first, PostgreSQL later
- Streamlit
- Plotly
- GitHub

## Project Structure

```text
fieldops-analytics-os/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── generate_data.py
│   └── config.py
├── sql/
├── dashboard/
├── notebooks/
├── reports/
└── docs/

## v0.3 — SQLite Loader and SQL Analytics

This version adds a SQLite analytics layer.

### New Features

- Loads synthetic CSV data into a SQLite database
- Creates database tables for buyers, providers, work orders, payments, reviews, and support tickets
- Adds indexes for common analysis fields
- Adds SQL queries for marketplace finance and operational analysis
- Exports SQL query results into report CSV files

### How to Run

Generate data:

```bash
python src/generate_data.py

## v0.4 — Streamlit Executive Dashboard

This version adds an interactive Streamlit dashboard for executive marketplace analytics.

### Dashboard Sections

- Executive KPI Overview
- Monthly Revenue Trend
- Work Order Status Breakdown
- Revenue by Category
- Top Buyers
- Payment Delay Risk
- Top Locations
- Business Insights
- Dashboard Data Tables

### How to Run the Dashboard

Generate synthetic data:

```bash
python src/generate_data.py

## v0.5 — Finance Analytics Deep Dive

This version adds a deeper finance analytics layer to FieldOps Analytics OS.

### New Finance Features

- Monthly finance performance
- Gross Work Order Value trend
- Platform revenue trend
- Provider payout trend
- Take rate trend
- Average work order value trend
- Buyer revenue concentration
- Top buyers by platform revenue
- Category finance performance
- Payment delay risk analysis
- Finance insights report

### Finance KPIs

- Gross Work Order Value
- Platform Revenue
- Provider Payout
- Take Rate
- Average Work Order Value
- Buyer Revenue Share
- Payment Delay
- Late Payment Rate

### New SQL Queries

- `09_finance_monthly_deep_dive.sql`
- `10_take_rate_trend.sql`
- `11_buyer_revenue_concentration.sql`
- `12_payment_risk_summary.sql`
- `13_category_finance_performance.sql`

### Run the Project

```bash
python src/generate_data.py
python src/load_to_sqlite.py
python src/run_sql_queries.py
streamlit run dashboard/app.py