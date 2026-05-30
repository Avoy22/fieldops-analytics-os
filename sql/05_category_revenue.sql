-- Category revenue
-- Business question:
-- Which service categories create the most marketplace revenue?

SELECT
    category,
    COUNT(work_order_id) AS total_work_orders,
    SUM(CASE WHEN status IN ('completed', 'approved') THEN 1 ELSE 0 END) AS successful_orders,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(SUM(total_amount), 2) AS gross_work_order_value,
    ROUND(SUM(platform_fee), 2) AS platform_revenue,
    ROUND(SUM(provider_payout), 2) AS provider_payout,
    ROUND(AVG(total_amount), 2) AS average_order_value,
    ROUND(AVG(take_rate), 4) AS average_take_rate
FROM work_orders
GROUP BY category
ORDER BY platform_revenue DESC;
