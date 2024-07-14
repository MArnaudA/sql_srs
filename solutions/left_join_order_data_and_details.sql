SELECT * FROM orders
LEFT JOIN order_details
USING (order_id)