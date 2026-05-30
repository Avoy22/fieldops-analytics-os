-- Monthly revenue KPIs
-- Business question:
-- How much marketplace revenue is generated each month?

SELECT
    strftime('%Y-%m', created_at) AS month,
    COUNT(work_order_id) AS total_work_orders,
    SUM(CASE WHEN status IN ('completed', 'approved') THEN 1 ELSE 0 END) AS completed_or_approved_orders,
    ROUND(SUM(total_amount), 2) AS gross_work_order_value,
    ROUND(SUM(platform_fee), 2) AS platform_revenue,
    ROUND(SUM(provider_payout), 2) AS provider_payout,
    ROUND(AVG(total_amount), 2) AS average_work_order_value,
    ROUND(
        SUM(platform_fee) * 1.0 / NULLIF(SUM(total_amount), 0),
        4
    ) AS take_rate
FROM work_orders
GROUP BY strftime('%Y-%m', created_at)
ORDER BY month;