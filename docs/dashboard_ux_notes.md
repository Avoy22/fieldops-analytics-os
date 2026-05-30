# Dashboard UX Notes

FieldOps Analytics OS v0.7 improves the dashboard from a static executive view into a more interactive analysis tool.

## UX Goals

- Let stakeholders explore the same dashboard from different business angles.
- Keep the first screen useful for portfolio reviewers.
- Preserve the existing executive dashboard and finance deep dive sections.
- Keep the Streamlit code readable for beginner-friendly review.

## Interactive Dataset

The new top dashboard section uses a joined SQLite dataset from:

- `work_orders`
- `buyers`
- `payments`

The joined view keeps work-order grain as the main analytical grain, then adds buyer attributes and payment timing fields.

## Sidebar Filters

The sidebar filters are:

- Created date range
- Service category
- Work order status
- Buyer industry
- Country

These filters apply to the interactive section at the top of the dashboard. The existing executive dashboard and finance deep dive remain full-dataset views for consistent baseline reporting.

## Filtered Metrics

The filtered KPI cards show:

- Filtered Work Orders
- Gross Work Order Value
- Platform Revenue
- Provider Payout
- Take Rate
- Success Rate
- Cancellation Rate
- Average Payment Delay

This gives reviewers an immediate read on how the selected segment compares across volume, monetization, operations, and payment behavior.

## Filtered Charts

The interactive chart set includes:

- Monthly revenue trend
- Status breakdown
- Platform revenue by category
- Top buyers by platform revenue

These charts were selected because they answer common marketplace questions quickly: when revenue is created, which statuses dominate, which services monetize best, and which accounts drive platform revenue.

## Export and Glossary

The CSV download button exports the active filtered dataset for offline review. The metric glossary uses `st.expander` so KPI definitions are available without cluttering the main dashboard.

## Screenshot Recommendations

Capture the dashboard with the sidebar visible so the filterable UX is obvious. Suggested screenshots:

- `assets/screenshots/interactive-dashboard.png`
- `assets/screenshots/executive-dashboard.png`
- `assets/screenshots/finance-deep-dive.png`
- `assets/screenshots/buyer-concentration.png`
- `assets/screenshots/payment-risk.png`

