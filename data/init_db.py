import io

import duckdb
import pandas as pd

conn = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------------

data = {
    "theme" : ["Cross Joins", "Window Functions"],
    "exercise_name" : ["beverages_and_food", "simple_window"],
    "tables" : [["beverages", "food_items"], ["simple_window"]],
    "last_reviewed" : ["2021-09-01", "2021-09-01"]
}
memory_state_df = pd.DataFrame(data)
conn.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")

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
