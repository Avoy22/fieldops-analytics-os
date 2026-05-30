-- Top buyers by marketplace value
-- Business question:
-- Which buyer companies generate the most work order value?

SELECT
    b.buyer_id,
    b.company_name,
    b.industry,
    b.buyer_tier,
    b.city,
    b.state,
    COUNT(w.work_order_id) AS total_work_orders,
    SUM(CASE WHEN w.status IN ('completed', 'approved') THEN 1 ELSE 0 END) AS successful_orders,
    ROUND(SUM(w.total_amount), 2) AS gross_work_order_value,
    ROUND(SUM(w.platform_fee), 2) AS platform_revenue,
    ROUND(AVG(w.total_amount), 2) AS average_order_value
FROM buyers b
JOIN work_orders w
    ON b.buyer_id = w.buyer_id
GROUP BY
    b.buyer_id,
    b.company_name,
    b.industry,
    b.buyer_tier,
    b.city,
    b.state
ORDER BY gross_work_order_value DESC
LIMIT 20;
