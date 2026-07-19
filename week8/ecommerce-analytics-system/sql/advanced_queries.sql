-- 7. Running total of revenue using Window Function

SELECT
    o.status,
    DATE(o.order_date) AS order_date,
    ROUND(SUM(
        oi.quantity * oi.unit_price *
        (1 - oi.discount_percent / 100.0)
    ),2) AS daily_revenue,

    ROUND(
        SUM(
            SUM(
                oi.quantity * oi.unit_price *
                (1 - oi.discount_percent / 100.0)
            )
        ) OVER(
            PARTITION BY o.status
            ORDER BY DATE(o.order_date)
        ),
        2
    ) AS running_total

FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id

GROUP BY
    o.status,
    DATE(o.order_date);



-- 8. Rank products by revenue inside category using DENSE_RANK

WITH product_sales AS
(
    SELECT
        p.category,
        p.product_name,
        SUM(
            oi.quantity * oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) AS total_revenue

    FROM order_items oi
    JOIN products p
    ON oi.product_id = p.product_id

    GROUP BY
        p.category,
        p.product_name
)

SELECT
    category,
    product_name,
    ROUND(total_revenue,2) AS total_revenue,

    DENSE_RANK() OVER(
        PARTITION BY category
        ORDER BY total_revenue DESC
    ) AS rank_in_category

FROM product_sales;



-- 9. Days between consecutive customer orders using LAG

WITH customer_orders AS
(
    SELECT
        customer_id,
        DATE(order_date) AS order_date,

        LAG(DATE(order_date))
        OVER(
            PARTITION BY customer_id
            ORDER BY order_date
        ) AS previous_order_date

    FROM orders
)

SELECT
    customer_id,
    order_date,
    previous_order_date,

    JULIANDAY(order_date)
    -
    JULIANDAY(previous_order_date)
    AS days_gap

FROM customer_orders;



-- 10. CTE Multiple Levels - Monthly customer revenue category

WITH monthly_customer_revenue AS
(
    SELECT
        strftime('%Y-%m',o.order_date) AS month,
        o.customer_id,

        SUM(
            oi.quantity * oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) AS revenue

    FROM orders o
    JOIN order_items oi
    ON o.order_id = oi.order_id

    GROUP BY
        month,
        o.customer_id
),

customer_category AS
(
    SELECT
        month,
        customer_id,
        revenue,

        CASE
            WHEN revenue > 10000 THEN 'High'
            WHEN revenue BETWEEN 5000 AND 10000 THEN 'Medium'
            ELSE 'Low'
        END AS category

    FROM monthly_customer_revenue
)

SELECT
    month,
    category,
    COUNT(customer_id) AS customer_count

FROM customer_category

GROUP BY
    month,
    category;



-- 11. NTILE Customer Segmentation

WITH customer_value AS
(
    SELECT
        customer_id,

        SUM(
            oi.quantity * oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) AS total_value

    FROM orders o
    JOIN order_items oi
    ON o.order_id = oi.order_id
    WHERE customer_id != 'UNKNOWN'
    
    GROUP BY customer_id
)

SELECT
    customer_id,
    ROUND(total_value,2),

    NTILE(4) OVER(
        ORDER BY total_value DESC
    ) AS quartile,

    CASE
        WHEN NTILE(4) OVER(ORDER BY total_value DESC)=1
        THEN 'Platinum'

        WHEN NTILE(4) OVER(ORDER BY total_value DESC)=2
        THEN 'Gold'

        WHEN NTILE(4) OVER(ORDER BY total_value DESC)=3
        THEN 'Silver'

        ELSE 'Bronze'
    END AS quartile_label

FROM customer_value;



-- 12. Year over Year Revenue Comparison

WITH monthly_revenue AS
(
    SELECT
        strftime('%Y',o.order_date) AS year,
        strftime('%m',o.order_date) AS month,

        SUM(
            oi.quantity * oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) AS revenue

    FROM orders o
    JOIN order_items oi
    ON o.order_id = oi.order_id

    GROUP BY year,month
)

SELECT
    year,
    month,
    ROUND(revenue,2) AS revenue,

    ROUND(
        LAG(revenue) OVER(
            PARTITION BY month
            ORDER BY year
        ),
        2
    ) AS prev_year_revenue,

    ROUND(
        (
        revenue -
        LAG(revenue) OVER(
            PARTITION BY month
            ORDER BY year
        )
        )
        /
        LAG(revenue) OVER(
            PARTITION BY month
            ORDER BY year
        )
        *100,
        2
    ) AS yoy_growth_percent

FROM monthly_revenue;



-- 13. First and Last Purchased Category

WITH category_orders AS
(
    SELECT
        o.customer_id,
        p.category,
        o.order_date,

        FIRST_VALUE(p.category)
        OVER(
            PARTITION BY o.customer_id
            ORDER BY o.order_date
        ) AS first_category,

        LAST_VALUE(p.category)
        OVER(
            PARTITION BY o.customer_id
            ORDER BY o.order_date
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND UNBOUNDED FOLLOWING
        ) AS last_category

    FROM orders o
    JOIN order_items oi
    ON o.order_id=oi.order_id

    JOIN products p
    ON oi.product_id=p.product_id
)

SELECT DISTINCT
    customer_id,
    first_category,
    last_category,

    CASE
        WHEN first_category != last_category
        THEN 'Yes'
        ELSE 'No'
    END AS category_shift

FROM category_orders;



-- 14. Cumulative Revenue Percentage

WITH customer_revenue AS
(
    SELECT
        o.customer_id,

        SUM(
            oi.quantity * oi.unit_price *
            (1 - oi.discount_percent / 100.0)
        ) AS revenue

    FROM orders o
    JOIN order_items oi
    ON o.order_id=oi.order_id

    GROUP BY customer_id
)

SELECT
    customer_id,
    ROUND(revenue,2),

    ROUND(
        SUM(revenue) OVER(
            ORDER BY revenue DESC
        ),
        2
    ) AS cumulative_revenue,

    ROUND(
        SUM(revenue) OVER(
            ORDER BY revenue DESC
        )
        /
        SUM(revenue) OVER()
        *100,
        2
    ) AS cumulative_percent

FROM customer_revenue;



-- 15. Cohort Analysis

WITH customer_cohort AS
(
    SELECT
        customer_id,

        strftime(
            '%Y-%m',
            MIN(order_date)
        ) AS cohort_month

    FROM orders

    GROUP BY customer_id
),

activity AS
(
    SELECT
        o.customer_id,

        c.cohort_month,

        strftime('%Y-%m',o.order_date)
        AS order_month

    FROM orders o

    JOIN customer_cohort c
    ON o.customer_id=c.customer_id
)

SELECT
    cohort_month,
    order_month,

    COUNT(DISTINCT customer_id)
    AS customers

FROM activity

GROUP BY
    cohort_month,
    order_month;



-- 16. Self Join Customer Repeat Analysis

SELECT
    a.customer_id,

    COUNT(DISTINCT a.order_id)
    AS first_orders,

    COUNT(DISTINCT b.order_id)
    AS repeat_orders

FROM orders a

LEFT JOIN orders b

ON a.customer_id=b.customer_id
AND b.order_date>a.order_date

GROUP BY a.customer_id;