-- 1. Total revenue per category

SELECT
    p.category,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_revenue
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;


-- 2. Top 10 customers by total order value

SELECT
    o.customer_id,
    ROUND(
        SUM(
            oi.quantity *
            oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_order_value
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
WHERE o.customer_id != 'UNKNOWN'
GROUP BY o.customer_id
ORDER BY total_order_value DESC
LIMIT 10;


-- 3. Month-wise order count for last 12 months

SELECT
    strftime('%Y-%m', order_date) AS month,
    COUNT(*) AS order_count
FROM orders
GROUP BY month
ORDER BY month DESC
LIMIT 12;