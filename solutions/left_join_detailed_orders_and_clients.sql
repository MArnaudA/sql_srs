WITH detailed_order AS (
    
    SELECT * FROM orders
    LEFT JOIN order_details
    USING (order_id)

)

SELECT customers.customer_id,
customer_name,
order_id,
product_id,
quantity
FROM customers
LEFT JOIN detailed_order
USING (customer_id)