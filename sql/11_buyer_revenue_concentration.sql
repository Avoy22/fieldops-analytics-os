-- Buyer revenue concentration
-- Business question:
-- Is the marketplace too dependent on a small number of buyers?

WITH buyer_revenue AS (
    SELECT
        b.buyer_id,
        b.company_name,
        b.industry,
        COUNT(w.work_order_id) AS total_work_orders,
        ROUND(SUM(w.total_amount), 2) AS gross_work_order_value,
        ROUND(SUM(w.platform_fee), 2) AS platform_revenue
    FROM work_orders w
    JOIN buyers b
        ON w.buyer_id = b.buyer_id
    GROUP BY
        b.buyer_id,
        b.company_name,
        b.industry
),

ranked_buyers AS (
    SELECT
        *,
        RANK() OVER (ORDER BY platform_revenue DESC) AS revenue_rank,
        SUM(platform_revenue) OVER () AS total_platform_revenue
    FROM buyer_revenue
)

SELECT
    buyer_id,
    company_name,
    industry,
    revenue_rank,
    total_work_orders,
    gross_work_order_value,
    platform_revenue,

    ROUND(
        platform_revenue * 100.0 / NULLIF(total_platform_revenue, 0),
        2
    ) AS revenue_share_pct

FROM ranked_buyers
ORDER BY platform_revenue DESC
LIMIT 25;