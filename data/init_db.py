import io

import duckdb
import pandas as pd

conn = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------------

data = {
    "theme": 
    [
        "Cross Joins",
        "Cross Joins", 
        "Inner Joins", 
        "Inner Joins", 
        "Inner Joins"
    ],
    "exercise_name": 
    [
        "beverages_and_food", 
        "sizes_and_trademarks", 
        "order_data_and_details",
        "detailed_orders_and_clients",
        "detailed_orders_clients_and_products"
    ],
    "tables": 
    [
        ["beverages", "food_items"],
        ["sizes", "trademark"],
        ["orders", "order_details"],
        ["orders", "order_details", "customers"],
        ["orders", "order_details", "customers", "products"]
    ],
    "last_reviewed": 
    [
        "2021-09-01", 
        "2021-09-01",
        "2021-09-01",
        "2021-09-01",
        "2021-09-01"
    ],
    "question": [
        "Query all the combinations of beverages and food items", 
        "Query all the combinations of sizes and trademarks",
        "Join the orders and order_details tables",
        "Get the detailed orders and clients information (Tips : CTE)",
        "Get the detailed orders and clients information with products (Tips : CTE)"
        ]
}
memory_state_df = pd.DataFrame(data)
conn.execute(
    "CREATE OR REPLACE TABLE memory_state AS SELECT * FROM memory_state_df ORDER by last_reviewed"
)

# ------------------------------------------------------------------
# CROSS JOIN EXERCISES
# ------------------------------------------------------------------
csv = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""

beverages = pd.read_csv(io.StringIO(csv))
conn.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

csv2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""

food_items = pd.read_csv(io.StringIO(csv2))
conn.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

csv3 = """
size
XS
S
M
L
XL
"""

sizes = pd.read_csv(io.StringIO(csv3))
conn.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes")

csv4 = """
trademark
Nike
Asphalte
Abercrombie
Levis
"""

trademarks = pd.read_csv(io.StringIO(csv4))
conn.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks")

# ------------------------------------------------------------------
# INNER JOIN EXERCISES
# ------------------------------------------------------------------

# Exercise 1 

orders_data = {
    'order_id': [1, 2, 3, 4, 5],
    'customer_id': [101, 102, 103, 104, 105]
}
orders = pd.DataFrame(orders_data)
conn.execute("CREATE TABLE IF NOT EXISTS orders AS SELECT * FROM orders")

customers_data = {
    'customer_id': [101, 102, 103, 104, 105, 106],
    'customer_name': ["Toufik", "Daniel", "Tancrède", "Kaouter", "Jean-Nicolas", "David"]
}
customers = pd.DataFrame(customers_data)
conn.execute("CREATE TABLE IF NOT EXISTS customers AS SELECT * FROM customers")

p_names = ["Laptop", "Ipad", "Livre", "Petitos"]
products_data = {
    'product_id': [101, 103, 104, 105],
    'product_name': p_names,
    'product_price': [800, 400, 30, 2]
}
products = pd.DataFrame(products_data)
conn.execute("CREATE TABLE IF NOT EXISTS products AS SELECT * FROM products")

order_details_data = {
    'order_id': [1, 2, 3, 4, 5],
    'product_id': [102, 104, 101, 103, 105],
    'quantity': [2, 1, 3, 2, 1]
}
order_details = pd.DataFrame(order_details_data)
conn.execute("CREATE TABLE IF NOT EXISTS order_details AS SELECT * FROM order_details")





