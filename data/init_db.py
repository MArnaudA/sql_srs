import io

import duckdb
import pandas as pd

conn = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------------

data = {
    "theme": ["Cross Joins", "Cross Joins"],
    "exercise_name": ["beverages_and_food", "sizes_and_trademarks"],
    "tables": [["beverages", "food_items"], ["sizes", "trademark"]],
    "last_reviewed": ["2022-09-01", "2021-09-01"],
    "question": [
        "Query all the combinations of beverages and food items", 
        "Query all the combinations of sizes and trademarks"
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
