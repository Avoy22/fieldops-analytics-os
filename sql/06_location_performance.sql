-- Location performance
-- Business question:
-- Which markets have the strongest work order volume and revenue?

SELECT
    city,
    state,
    country,
    COUNT(work_order_id) AS total_work_orders,
    SUM(CASE WHEN status IN ('completed', 'approved') THEN 1 ELSE 0 END) AS successful_orders,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(
        SUM(CASE WHEN status IN ('completed', 'approved') THEN 1 ELSE 0 END) * 100.0
        / NULLIF(COUNT(work_order_id), 0),
        2
    ) AS success_rate_pct,
    ROUND(SUM(total_amount), 2) AS gross_work_order_value,
    ROUND(SUM(platform_fee), 2) AS platform_revenue,
    ROUND(AVG(total_amount), 2) AS average_order_value
FROM work_orders
GROUP BY
    city,
    state,
    country
ORDER BY platform_revenue DESC;
