-- Marketplace health
-- Business question:
-- What is the monthly health trend across demand, success, payments, reviews, and support?

WITH monthly_work_orders AS (
    SELECT
        strftime('%Y-%m', created_at) AS month,
        COUNT(work_order_id) AS total_work_orders,
        SUM(CASE WHEN status IN ('completed', 'approved') THEN 1 ELSE 0 END) AS successful_orders,
        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
        ROUND(SUM(total_amount), 2) AS gross_work_order_value,
        ROUND(SUM(platform_fee), 2) AS platform_revenue
    FROM work_orders
    GROUP BY strftime('%Y-%m', created_at)
),
monthly_payments AS (
    SELECT
        strftime('%Y-%m', payment_due_date) AS month,
        COUNT(payment_id) AS total_payments,
        SUM(CASE WHEN payment_status = 'late' THEN 1 ELSE 0 END) AS late_payments,
        ROUND(AVG(days_to_pay), 2) AS average_days_to_pay
    FROM payments
    GROUP BY strftime('%Y-%m', payment_due_date)
),
monthly_reviews AS (
    SELECT
        strftime('%Y-%m', review_date) AS month,
        COUNT(review_id) AS review_count,
        ROUND(AVG(rating), 2) AS average_rating
    FROM reviews
    GROUP BY strftime('%Y-%m', review_date)
),
monthly_tickets AS (
    SELECT
        strftime('%Y-%m', opened_at) AS month,
        COUNT(ticket_id) AS support_tickets,
        SUM(CASE WHEN status = 'escalated' THEN 1 ELSE 0 END) AS escalated_tickets
    FROM support_tickets
    GROUP BY strftime('%Y-%m', opened_at)
)
SELECT
    w.month,
    w.total_work_orders,
    w.successful_orders,
    w.cancelled_orders,
    ROUND(w.successful_orders * 100.0 / NULLIF(w.total_work_orders, 0), 2) AS success_rate_pct,
    ROUND(w.cancelled_orders * 100.0 / NULLIF(w.total_work_orders, 0), 2) AS cancellation_rate_pct,
    w.gross_work_order_value,
    w.platform_revenue,
    COALESCE(p.total_payments, 0) AS total_payments,
    COALESCE(p.late_payments, 0) AS late_payments,
    p.average_days_to_pay,
    COALESCE(r.review_count, 0) AS review_count,
    r.average_rating,
    COALESCE(t.support_tickets, 0) AS support_tickets,
    COALESCE(t.escalated_tickets, 0) AS escalated_tickets
FROM monthly_work_orders w
LEFT JOIN monthly_payments p
    ON w.month = p.month
LEFT JOIN monthly_reviews r
    ON w.month = r.month
LEFT JOIN monthly_tickets t
    ON w.month = t.month
ORDER BY w.month;
