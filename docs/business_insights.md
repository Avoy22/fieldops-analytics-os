# Business Insights

This document summarizes how FieldOps Analytics OS translates marketplace data into business recommendations. The insights are based on synthetic data, but the analytical patterns mirror common finance, BI, and operations questions in a real marketplace business.

## Executive KPI Interpretation

| KPI | Interpretation |
| --- | --- |
| Gross Work Order Value | Measures total marketplace transaction volume. It is useful for scale, but it does not show revenue quality by itself. |
| Platform Revenue | Measures the marketplace revenue retained through platform fees. This is the primary revenue metric. |
| Provider Payout | Shows how much value flows through to service providers. It should be reviewed with platform revenue to understand margin pressure. |
| Take Rate | Shows monetization efficiency. A stable or intentionally managed take rate is important for revenue predictability. |
| Average Work Order Value | Helps identify pricing, category mix, enterprise account influence, and premium service lines. |
| Success Rate | Shows whether work orders are moving through the marketplace successfully. |
| Cancellation Rate | Signals operational friction, buyer churn risk, or provider capacity issues. |
| Buyer Revenue Share | Measures concentration risk and account dependency. |
| Late Payment Rate | Tracks collections risk and cash-flow reliability. |
| Average Payment Delay | Measures severity of late payment behavior after the due date. |

## Current Sample Insights

The current seeded dataset shows:

- 10,000 work orders.
- Approximately $13.3M in gross work order value.
- Approximately $2.3M in platform revenue.
- Approximately $11.1M in provider payout.
- Overall take rate near 17%.
- 62.45% work order success rate.
- 8.79% cancellation rate.
- Roofing as the highest platform revenue category.
- Low concentration among the largest buyers in the current sample.
- Several buyers with high payment risk based on late payments and average delay.

These values may change if the synthetic data generation logic or seed changes.

## Revenue Quality

Gross work order value should not be interpreted as revenue. The finance view separates:

- Gross Work Order Value
- Platform Revenue
- Provider Payout

This distinction is important because a marketplace can grow transaction volume while platform revenue grows more slowly if the business shifts into lower-fee categories or offers lower negotiated rates to large buyers.

Recommended action:

- Review platform revenue growth alongside gross work order value and provider payout every month.

## Take Rate Stability

Take rate is one of the most important marketplace finance metrics.

```text
Take Rate = Platform Revenue / Gross Work Order Value
```

A declining take rate is not automatically bad. It may reflect enterprise expansion, strategic pricing, or category mix shifts. The risk is when take rate erosion is hidden inside overall volume growth.

Recommended action:

- Track take rate by month and category to identify pricing or mix changes early.

## Buyer Concentration

Buyer concentration turns a sales leaderboard into a finance risk view. A high-value buyer can be good for growth, but excessive dependence on a small number of buyers creates renewal, churn, and cash-flow exposure.

Recommended action:

- Monitor top 5 and top 10 buyer revenue share.
- Review account health for high-value buyers.
- Pair buyer revenue share with payment risk and support activity.

## Payment Risk

Late and pending payments affect cash predictability. Buyers with high revenue and high late-payment rates deserve special attention because they combine commercial value with collections risk.

Recommended action:

- Prioritize buyers with high platform revenue, high late-payment rates, and high average payment delay.
- Use payment risk levels to guide collections review and credit policy.

## Category Performance

Category analysis helps the business identify where growth is financially attractive and operationally sustainable.

Strong categories may show:

- High platform revenue
- High average work order value
- Stable take rate
- Strong success rate

Weak categories may show:

- Low revenue despite high volume
- Lower take rate
- High cancellation rate
- Lower success rate

Recommended action:

- Use category finance performance to guide provider recruiting, sales focus, and pricing review.

## Operational Health

Finance metrics should be reviewed with operational metrics. Revenue growth is less valuable if it comes with lower success rates, high cancellations, poor provider quality, or high support volume.

Recommended action:

- Review success rate, cancellation rate, reviews, support tickets, and payment performance together in monthly business reviews.

## Analyst Talking Points

For a portfolio walkthrough, this project can be explained as:

- "I designed a synthetic marketplace dataset and used it to build a repeatable BI workflow."
- "I separated gross marketplace volume from actual platform revenue so the dashboard reflects finance reality."
- "I added buyer concentration and payment risk analysis because revenue growth can create hidden account and cash-flow risk."
- "I wrote SQL queries around business questions, not just tables."
- "I built documentation so stakeholders can understand the model, metrics, dashboard, and recommendations."

