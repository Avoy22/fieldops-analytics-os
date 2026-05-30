# FieldOps Analytics OS - Finance Insights Report

## Purpose

This report documents the finance analytics layer for FieldOps Analytics OS. It is written for Data Analyst, BI Analyst, and Finance Analytics portfolio review, with an emphasis on marketplace revenue quality, buyer concentration, category performance, and payment delay risk.

## KPI Definitions

| KPI | Definition | Why it matters |
| --- | --- | --- |
| Gross Work Order Value | Total dollar value of all work orders. | Measures marketplace transaction volume before fees and payouts. |
| Platform Revenue | Total platform fee collected from work orders. | Represents the marketplace's revenue stream. |
| Provider Payout | Gross work order value minus platform revenue. | Shows how much value flows through to service providers. |
| Take Rate | Platform revenue divided by gross work order value. | Measures monetization efficiency. |
| Average Work Order Value | Gross work order value divided by work order count. | Helps identify pricing, category mix, and enterprise account impact. |
| Success Rate | Completed or approved work orders divided by total work orders. | Connects finance performance to operational execution. |
| Buyer Revenue Share | A buyer's platform revenue divided by total platform revenue. | Highlights customer concentration risk. |
| Late Payment Rate | Late payments divided by total payments. | Tracks collections and cash-flow risk. |
| Average Payment Delay | Average days paid after the 30-day due date. | Quantifies how severe payment delays are when they occur. |

## Analyst Findings to Monitor

### Revenue Growth

Monthly gross work order value, platform revenue, and provider payout should be reviewed together. If gross work order value grows but platform revenue does not, the business may be adding volume in lower-fee categories or with lower negotiated take rates.

### Take Rate Discipline

The take rate trend should remain reasonably stable over time. A declining take rate can be acceptable if it is tied to strategic enterprise growth, but it should be visible and intentional rather than hidden inside blended revenue growth.

### Buyer Concentration

Top-buyer revenue share is a finance risk metric, not just a sales leaderboard. If the top 5 or top 10 buyers contribute a large share of platform revenue, leadership should monitor renewal exposure, account health, and payment behavior closely.

### Category Performance

Categories with high platform revenue and high average work order value are strong candidates for provider recruiting and sales expansion. Categories with high volume but weaker revenue may need pricing, packaging, or operational review.

### Payment Risk

Late and pending payments affect cash predictability. Buyers with high platform revenue and high payment delay deserve priority review because they combine revenue importance with collections risk.

## Recommendations

1. Review top 5 and top 10 buyer revenue share monthly to understand concentration risk.
2. Track take rate by month and category so pricing changes are visible early.
3. Compare average work order value by category to identify premium service lines.
4. Prioritize collections follow-up for buyers with high platform revenue, high late payment rates, and high average payment delay.
5. Use category finance performance to guide provider supply planning and go-to-market focus.
6. Pair finance KPIs with operational KPIs so revenue growth is not evaluated separately from completion quality.

## SQL Assets

The finance deep dive is powered by these SQL files:

- `sql/09_finance_monthly_deep_dive.sql`
- `sql/10_take_rate_trend.sql`
- `sql/11_buyer_revenue_concentration.sql`
- `sql/12_payment_risk_summary.sql`
- `sql/13_category_finance_performance.sql`
