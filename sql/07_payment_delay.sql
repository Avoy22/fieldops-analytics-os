-- Payment delay analysis
-- Business question:
-- How quickly do buyers pay, and where are late payments concentrated?

SELECT
    b.buyer_id,
    b.company_name,
    b.industry,
    COUNT(p.payment_id) AS total_payments,
    SUM(CASE WHEN p.payment_status = 'paid' THEN 1 ELSE 0 END) AS paid_payments,
    SUM(CASE WHEN p.payment_status = 'late' THEN 1 ELSE 0 END) AS late_payments,
    SUM(CASE WHEN p.payment_status = 'pending' THEN 1 ELSE 0 END) AS pending_payments,
    ROUND(
        SUM(CASE WHEN p.payment_status = 'late' THEN 1 ELSE 0 END) * 100.0
        / NULLIF(COUNT(p.payment_id), 0),
        2
    ) AS late_payment_rate_pct,
    ROUND(AVG(p.days_to_pay), 2) AS average_days_to_pay,
    ROUND(SUM(p.total_amount), 2) AS payment_value,
    ROUND(SUM(p.platform_fee), 2) AS platform_revenue
FROM payments p
JOIN buyers b
    ON p.buyer_id = b.buyer_id
GROUP BY
    b.buyer_id,
    b.company_name,
    b.industry
HAVING COUNT(p.payment_id) >= 3
ORDER BY late_payment_rate_pct DESC, payment_value DESC
LIMIT 25;
