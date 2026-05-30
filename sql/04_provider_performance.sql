-- Provider performance
-- Business question:
-- Which providers complete the most work and earn the strongest payouts?

SELECT
    p.provider_id,
    p.provider_name,
    p.business_type,
    p.primary_category,
    p.city,
    p.state,
    COUNT(w.work_order_id) AS total_work_orders,
    SUM(CASE WHEN w.status = 'completed' THEN 1 ELSE 0 END) AS completed_orders,
    SUM(CASE WHEN w.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(
        SUM(CASE WHEN w.status IN ('completed', 'approved') THEN 1 ELSE 0 END) * 100.0
        / NULLIF(COUNT(w.work_order_id), 0),
        2
    ) AS success_rate_pct,
    ROUND(SUM(w.provider_payout), 2) AS provider_payout,
    ROUND(AVG(r.rating), 2) AS average_review_rating,
    COUNT(r.review_id) AS review_count
FROM providers p
JOIN work_orders w
    ON p.provider_id = w.provider_id
LEFT JOIN reviews r
    ON w.work_order_id = r.work_order_id
GROUP BY
    p.provider_id,
    p.provider_name,
    p.business_type,
    p.primary_category,
    p.city,
    p.state
HAVING COUNT(w.work_order_id) >= 3
ORDER BY provider_payout DESC
LIMIT 25;
