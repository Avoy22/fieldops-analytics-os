-- Work order health
-- Business question:
-- What is the completion, cancellation, and marketplace success rate?

SELECT
    COUNT(*) AS total_work_orders,

    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_orders,
    SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) AS approved_orders,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    SUM(CASE WHEN status = 'assigned' THEN 1 ELSE 0 END) AS assigned_orders,
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) AS pending_orders,

    ROUND(
        SUM(CASE WHEN status IN ('completed', 'approved') THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS success_rate_pct,

    ROUND(
        SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS cancellation_rate_pct
FROM work_orders;