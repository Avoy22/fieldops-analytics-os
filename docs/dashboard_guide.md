# Dashboard Guide

FieldOps Analytics OS uses Streamlit to present marketplace finance and operations metrics in an executive-friendly dashboard.

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

## Dashboard Purpose

The dashboard is designed to help a business stakeholder quickly understand:

- Marketplace scale
- Revenue and payout health
- Take rate performance
- Buyer concentration
- Payment delay risk
- Category performance
- Location performance
- Work order execution quality

## Required Data

The dashboard reads from:

```text
data/processed/fieldops.db
```

If the database is missing, run:

```bash
python src/generate_data.py
python src/load_to_sqlite.py
```

For SQL output exports, also run:

```bash
python src/run_sql_queries.py
```

## Main Sections

### Header

Introduces the dashboard as an executive marketplace finance and field-service operations view.

### Interactive Dashboard

The v0.7 interactive section appears near the top of the app and responds to sidebar filters. It is built from a joined SQLite dataset using:

- `work_orders`
- `buyers`
- `payments`

The section includes filtered KPI cards, filtered charts, a CSV export button, and a metric glossary.

Sidebar filters:

- Created date range
- Service category
- Work order status
- Buyer industry
- Country

Filtered KPI cards:

- Filtered Work Orders
- Gross Work Order Value
- Platform Revenue
- Provider Payout
- Take Rate
- Success Rate
- Cancellation Rate
- Average Payment Delay

Filtered charts:

- Monthly revenue trend
- Status breakdown
- Platform revenue by category
- Top buyers by platform revenue

### KPI Cards

Displays:

- Total Work Orders
- Gross Work Order Value
- Platform Revenue
- Provider Payout
- Take Rate
- Success Rate
- Cancellation Rate
- Average Payment Delay

### Revenue Trend

Shows monthly trends for:

- Gross Work Order Value
- Platform Revenue
- Provider Payout

This helps separate marketplace transaction volume from platform monetization and provider payout flow.

### Work Order Status

Shows the distribution of:

- Completed
- Approved
- Assigned
- Pending
- Cancelled

This helps leadership connect revenue performance to execution quality.

### Revenue by Category

Ranks service categories by gross work order value and supports questions about category expansion, pricing, and supply planning.

### Buyer Concentration

Shows top buyers by gross work order value and industry. This section supports account management and concentration-risk review.

### Payment Delay Risk

Ranks buyers by average payment delay after due date. This helps finance and operations teams identify buyers that may need collections follow-up or credit review.

### Top Locations

Ranks cities and markets by gross work order value. This supports market expansion and provider recruiting decisions.

### Data Tables

Provides tabbed data views for:

- Monthly Revenue
- Status Breakdown
- Category Revenue
- Top Buyers
- Payment Delay
- Locations

### Business Insights

Generates narrative insight text from the current dataset, including marketplace scale, operational health, revenue mix, buyer concentration, payment risk, and market footprint.

### Finance Analytics Deep Dive

Adds analyst-focused views for:

- Monthly finance performance
- Take rate trend by category
- Average work order value
- Top buyers by platform revenue
- Category finance performance
- Payment delay risk
- Finance analyst notes
- Finance data tables

## Screenshot Plan

Capture these images manually after the dashboard is running:

| Screenshot | Suggested dashboard area |
| --- | --- |
| `assets/screenshots/interactive-dashboard.png` | Top interactive dashboard with sidebar filters, filtered KPI cards, and revenue trend. |
| `assets/screenshots/executive-dashboard.png` | Top of dashboard with KPI cards and revenue trend. |
| `assets/screenshots/finance-deep-dive.png` | Finance Analytics Deep Dive header, KPI cards, and finance chart. |
| `assets/screenshots/buyer-concentration.png` | Buyer Concentration chart or Top Buyers by Platform Revenue chart. |
| `assets/screenshots/payment-risk.png` | Payment Delay Risk chart with risk levels visible. |

Recommended screenshot width: 1440px or wider for clean GitHub rendering.

## Dashboard Review Checklist

- Dashboard launches with `streamlit run dashboard/app.py`.
- Sidebar filters update the interactive KPI cards and charts.
- CSV export downloads the active filtered dataset.
- Metric glossary opens correctly.
- KPI cards load without database errors.
- Plotly charts render correctly.
- Finance deep dive section appears below the main executive dashboard.
- Data tables are populated.
- Screenshot files are saved using the exact names listed above.
- README image links render after screenshots are added.

