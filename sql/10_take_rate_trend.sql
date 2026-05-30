-- Take rate trend by month and category
-- Business question:
-- Is the platform take rate stable across categories and months?

SELECT
    strftime('%Y-%m', created_at) AS month,
    category,

    COUNT(work_order_id) AS total_work_orders,

    ROUND(SUM(total_amount), 2) AS gross_work_order_value,
    ROUND(SUM(platform_fee), 2) AS platform_revenue,

    ROUND(
        SUM(platform_fee) * 100.0 / NULLIF(SUM(total_amount), 0),
        2
    ) AS take_rate_pct,

    ROUND(AVG(total_amount), 2) AS average_order_value

FROM work_orders
GROUP BY
    strftime('%Y-%m', created_at),
    category
HAVING total_work_orders >= 5
ORDER BY month, platform_revenue DESC;