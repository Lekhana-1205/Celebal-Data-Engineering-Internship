-- 4. Customers who placed orders but never had any item delivered

SELECT DISTINCT o.customer_id
FROM orders o
WHERE o.customer_id IS NOT NULL
AND o.customer_id NOT IN (
    SELECT DISTINCT customer_id
    FROM orders
    WHERE status = 'DELIVERED'
);


-- 5. Products that had more returns than purchases

SELECT
    p.product_id,
    p.product_name,
    SUM(CASE WHEN oi.quantity > 0 THEN oi.quantity ELSE 0 END) AS purchased,
    ABS(SUM(CASE WHEN oi.quantity < 0 THEN oi.quantity ELSE 0 END)) AS returned
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name
HAVING returned > purchased;


-- 6. Return rate per category

SELECT
    p.category,
    ROUND(
        ABS(SUM(CASE WHEN oi.quantity < 0 THEN oi.quantity ELSE 0 END)) * 100.0 /
        SUM(ABS(oi.quantity)),
        2
    ) AS return_rate
FROM order_items oi
JOIN products p
ON oi.product_id = p.product_id
GROUP BY p.category;