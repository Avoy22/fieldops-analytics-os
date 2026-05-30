-- Payment risk summary
-- Business question:
-- Which buyers create the highest payment delay risk?

SELECT
    b.buyer_id,
    b.company_name,
    b.industry,

    COUNT(p.payment_id) AS total_payments,
    SUM(CASE WHEN p.payment_status = 'late' THEN 1 ELSE 0 END) AS late_payments,
    SUM(CASE WHEN p.payment_status = 'pending' THEN 1 ELSE 0 END) AS pending_payments,

    ROUND(SUM(w.total_amount), 2) AS gross_work_order_value,
    ROUND(SUM(w.platform_fee), 2) AS platform_revenue,

    ROUND(
        AVG(
            CASE
                WHEN p.days_to_pay IS NULL THEN NULL
                WHEN p.days_to_pay > 30 THEN p.days_to_pay - 30
                ELSE 0
            END
        ),
        2
    ) AS average_payment_delay_days,

    ROUND(
        SUM(CASE WHEN p.payment_status = 'late' THEN 1 ELSE 0 END) * 100.0
        / NULLIF(COUNT(p.payment_id), 0),
        2
    ) AS late_payment_rate_pct,

    ROUND(
        SUM(CASE WHEN p.payment_status IN ('late', 'pending') THEN 1 ELSE 0 END) * 100.0
        / NULLIF(COUNT(p.payment_id), 0),
        2
    ) AS payment_risk_rate_pct,

    CASE
        WHEN
            AVG(
                CASE
                    WHEN p.days_to_pay IS NULL THEN NULL
                    WHEN p.days_to_pay > 30 THEN p.days_to_pay - 30
                    ELSE 0
                END
            ) >= 20
            OR SUM(CASE WHEN p.payment_status = 'late' THEN 1 ELSE 0 END) * 100.0
                / NULLIF(COUNT(p.payment_id), 0) >= 35
            THEN 'High Risk'
        WHEN
            AVG(
                CASE
                    WHEN p.days_to_pay IS NULL THEN NULL
                    WHEN p.days_to_pay > 30 THEN p.days_to_pay - 30
                    ELSE 0
                END
            ) >= 10
            OR SUM(CASE WHEN p.payment_status = 'late' THEN 1 ELSE 0 END) * 100.0
                / NULLIF(COUNT(p.payment_id), 0) >= 20
            THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS payment_risk_level

FROM payments p
JOIN work_orders w
    ON p.work_order_id = w.work_order_id
JOIN buyers b
    ON w.buyer_id = b.buyer_id
GROUP BY
    b.buyer_id,
    b.company_name,
    b.industry
HAVING total_payments >= 3
ORDER BY average_payment_delay_days DESC
LIMIT 25;
