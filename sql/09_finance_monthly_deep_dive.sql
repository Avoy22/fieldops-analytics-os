-- Monthly finance deep dive
-- Business question:
-- How are revenue, platform fees, provider payouts, and average order values changing month by month?

SELECT
    strftime('%Y-%m', created_at) AS month,

    COUNT(work_order_id) AS total_work_orders,

    SUM(CASE WHEN status IN ('completed', 'approved') THEN 1 ELSE 0 END) AS successful_orders,

    ROUND(SUM(total_amount), 2) AS gross_work_order_value,
    ROUND(SUM(platform_fee), 2) AS platform_revenue,
    ROUND(SUM(provider_payout), 2) AS provider_payout,

    ROUND(AVG(total_amount), 2) AS average_work_order_value,
    ROUND(AVG(platform_fee), 2) AS average_platform_fee,
    ROUND(AVG(provider_payout), 2) AS average_provider_payout,

    ROUND(
        SUM(platform_fee) * 100.0 / NULLIF(SUM(total_amount), 0),
        2
    ) AS take_rate_pct,

    ROUND(
        SUM(provider_payout) * 100.0 / NULLIF(SUM(total_amount), 0),
        2
    ) AS provider_payout_rate_pct,

    ROUND(
        SUM(CASE WHEN status IN ('completed', 'approved') THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS success_rate_pct

FROM work_orders
GROUP BY strftime('%Y-%m', created_at)
ORDER BY month;