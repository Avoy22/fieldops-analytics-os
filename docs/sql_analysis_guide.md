# SQL Analysis Guide

The SQL layer turns the SQLite database into reusable business analysis outputs. Each SQL file answers one clear business question and can be run as part of the reporting workflow with:

```bash
python src/run_sql_queries.py
```

The runner reads `sql/*.sql`, executes each file against `data/processed/fieldops.db`, and exports results to `reports/query_outputs/*.csv`.

## Query Library

| File | Business question | Main output |
| --- | --- | --- |
| `01_revenue_kpis.sql` | How much marketplace revenue is generated each month? | Monthly work orders, gross value, platform revenue, provider payout, AOV, and take rate. |
| `02_work_order_health.sql` | What is the completion, cancellation, and success profile of the marketplace? | Status counts, success rate, and cancellation rate. |
| `03_top_buyers.sql` | Which buyer companies generate the most work order value? | Top buyers by gross value, platform revenue, volume, and AOV. |
| `04_provider_performance.sql` | Which providers complete the most work and earn the strongest payouts? | Provider workload, payout, success rate, cancellations, ratings, and review count. |
| `05_category_revenue.sql` | Which service categories create the most marketplace revenue? | Category volume, gross value, platform revenue, payout, AOV, and take rate. |
| `06_location_performance.sql` | Which markets have the strongest work order volume and revenue? | Location-level work orders, success rate, gross value, revenue, and AOV. |
| `07_payment_delay.sql` | How quickly do buyers pay, and where are late payments concentrated? | Buyer payment counts, late rate, average days to pay, payment value, and revenue. |
| `08_marketplace_health.sql` | What is the monthly health trend across demand, payments, reviews, and support? | Combined monthly work order, payment, review, and ticket metrics. |
| `09_finance_monthly_deep_dive.sql` | How are revenue, fees, payouts, and AOV changing month by month? | Monthly finance KPI table for dashboard deep dive. |
| `10_take_rate_trend.sql` | Is take rate stable across categories and months? | Monthly category take rate, volume, revenue, and AOV. |
| `11_buyer_revenue_concentration.sql` | Is the marketplace too dependent on a small number of buyers? | Buyer revenue ranking and platform revenue share. |
| `12_payment_risk_summary.sql` | Which buyers create the highest payment delay risk? | Buyer-level payment risk level, late rate, delay days, and revenue exposure. |
| `13_category_finance_performance.sql` | Which categories create the strongest financial performance? | Category revenue, payout, AOV, take rate, and success rate. |

## KPI Logic

| Metric | SQL logic |
| --- | --- |
| Gross Work Order Value | `SUM(total_amount)` |
| Platform Revenue | `SUM(platform_fee)` |
| Provider Payout | `SUM(provider_payout)` |
| Take Rate | `SUM(platform_fee) / SUM(total_amount)` |
| Average Work Order Value | `AVG(total_amount)` |
| Success Rate | Completed or approved work orders divided by total work orders |
| Cancellation Rate | Cancelled work orders divided by total work orders |
| Late Payment Rate | Late payments divided by total payments |
| Payment Risk Rate | Late or pending payments divided by total payments |
| Average Payment Delay | Average days paid after the 30-day due date |

## Analysis Themes

### Finance

Relevant files:

- `01_revenue_kpis.sql`
- `09_finance_monthly_deep_dive.sql`
- `10_take_rate_trend.sql`
- `13_category_finance_performance.sql`

Use these queries to understand growth, monetization, take rate stability, provider payout pressure, and category-level revenue quality.

### Marketplace Operations

Relevant files:

- `02_work_order_health.sql`
- `04_provider_performance.sql`
- `06_location_performance.sql`
- `08_marketplace_health.sql`

Use these queries to monitor operational performance, completion quality, location strength, and monthly health.

### Buyer and Payment Risk

Relevant files:

- `03_top_buyers.sql`
- `07_payment_delay.sql`
- `11_buyer_revenue_concentration.sql`
- `12_payment_risk_summary.sql`

Use these queries to identify high-value accounts, concentration risk, late-payment behavior, and credit or collections priorities.

## Analyst Workflow

1. Run the data generator.
2. Load the SQLite database.
3. Execute the SQL runner.
4. Review exported CSV files in `reports/query_outputs/`.
5. Compare SQL outputs against dashboard visuals.
6. Use the business insights documentation to frame findings for stakeholders.

## Notes for Reviewers

- All SQL is SQLite-compatible.
- Queries are intentionally readable and business-question oriented.
- Window functions are used where helpful, such as buyer revenue ranking and total revenue share.
- The query outputs are reproducible when the synthetic data seed remains unchanged.

