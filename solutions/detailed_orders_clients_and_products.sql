WITH detailed_orders AS (
    SELECT * FROM orders
    INNER JOIN order_details
    USING (order_id)
    ), 

WITH order_client AS(
    SELECT * FROM customers
    INNER JOIN detailed_orders
    USING (customer_id)
    )

SELECT * 
FROM order_client cc
INNER JOIN products
USING (product_id)