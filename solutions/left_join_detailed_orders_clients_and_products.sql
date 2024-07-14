WITH order_client AS (
    
    SELECT * FROM orders
    LEFT JOIN order_details
    USING (order_id)

),

WITH order_client AS (
    
    SELECT * FROM 
    USING (order_id)

),


SELECT * 
FROM order_client cc
LEFT JOIN products
ON cc.product_id = products.product_id