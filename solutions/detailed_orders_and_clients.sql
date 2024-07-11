WITH detailed_orders AS (
        
    SELECT * FROM orders
    INNER JOIN order_details
    USING (order_id)
        
    )

    SELECT * FROM customers
    INNER JOIN detailed_orders
    USING (customer_id)
