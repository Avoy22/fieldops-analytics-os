# FieldOps Analytics OS Case Study

## Executive Summary

FieldOps Analytics OS is a business intelligence case study for a simulated field-service marketplace. The project converts synthetic operational and financial data into a SQLite analytics database, reusable SQL analysis outputs, and an interactive Streamlit dashboard for executive reporting.

The goal is to demonstrate the work of a data analyst or BI analyst in a realistic business setting: define the business problem, design the dataset, calculate KPIs, build analysis queries, visualize performance, and translate the results into business recommendations.

## Business Context

A field-service marketplace connects companies that need on-site work with independent providers or vendors who complete jobs such as HVAC, plumbing, electrical, cleaning, landscaping, roofing, and security systems.

Marketplace leaders need visibility into both sides of the business:

- Demand from buyers
- Supply from providers
- Work order execution
- Platform revenue
- Provider payout
- Payment collection risk
- Support and review quality

Without a structured analytics layer, teams may see high transaction volume but miss deeper issues such as declining take rate, high provider payout pressure, buyer concentration, late payments, or weak category performance.

## Business Problem

The marketplace needs an analytics system that answers:

- Are work orders growing in a financially healthy way?
- Which buyers and categories drive platform revenue?
- Is revenue concentrated in a small number of buyers?
- Which buyers create cash-flow or collections risk?
- Are providers completing enough work at acceptable quality?
- Which locations and service categories deserve additional investment?
- How should leadership monitor finance and operations together?

## Project Objective

Build a complete local analytics workflow that simulates how a business intelligence team would support marketplace finance and operations.

The project delivers:

- A reproducible synthetic marketplace dataset
- A SQLite database for relational analysis
- A SQL query library for finance, operations, buyer, provider, category, location, and payment analysis
- Exported query outputs for reporting
- A Streamlit dashboard for executive review
- Business documentation for portfolio review

## Target Stakeholders

| Stakeholder | Questions answered |
| --- | --- |
| Executive leadership | Is the marketplace growing in a healthy and sustainable way? |
| Finance team | What are revenue, take rate, payout, and payment risk trends? |
| BI team | What metrics, queries, and dashboard views support recurring reporting? |
| Marketplace operations | Which categories, locations, buyers, and providers need attention? |
| Customer success | Which buyers are valuable, risky, or operationally complex? |

## Analytical Approach

1. Generate synthetic marketplace data with realistic buyer, provider, work order, payment, review, and support relationships.
2. Load raw CSV files into SQLite tables.
3. Create indexes for common analytical joins and filters.
4. Run SQL files that answer specific business questions.
5. Export query results as CSV files for review and documentation.
6. Build a Streamlit dashboard with KPI cards, charts, tables, and written insights.
7. Document the data model, architecture, SQL layer, dashboard views, and business recommendations.

## Current Sample Findings

The current seeded dataset produces the following example results:

- 10,000 generated work orders
- Approximately $13.3M in gross work order value
- Approximately $2.3M in platform revenue
- Approximately $11.1M in provider payout
- Overall take rate near 17%
- 62.45% work order success rate
- 8.79% cancellation rate
- Roofing as the top category by platform revenue
- Low top-buyer concentration in the current sample
- Multiple high-risk buyers based on payment delay and late-payment rate

These findings are based on synthetic data and should be read as analytical examples rather than real company performance.

## Deliverables

| Deliverable | Location |
| --- | --- |
| Data generator | `src/generate_data.py` |
| SQLite loader | `src/load_to_sqlite.py` |
| SQL runner | `src/run_sql_queries.py` |
| SQL analysis files | `sql/*.sql` |
| Query outputs | `reports/query_outputs/*.csv` |
| Dashboard | `dashboard/app.py` |
| Documentation | `README.md`, `docs/*.md`, `reports/finance_insights.md` |

## Role Alignment

This project is designed to demonstrate skills relevant to:

- **Data Analyst:** data cleaning, KPI definition, SQL analysis, and insight communication.
- **Business Intelligence Analyst:** data model documentation, dashboard design, reporting logic, and stakeholder storytelling.
- **Finance Analyst:** revenue, payout, take rate, concentration, and payment-risk analysis.
- **Marketplace Operations Analyst:** buyer, provider, category, location, work-order, and support performance analysis.

## Recommendations

- Review take rate by month and category to detect pricing or mix changes.
- Track top buyer revenue share monthly to manage concentration risk.
- Monitor payment risk by buyer and prioritize collections outreach for high-revenue late payers.
- Use category finance performance to guide sales focus and provider recruiting.
- Pair finance KPIs with success and cancellation rates so growth is not separated from operational health.

