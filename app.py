import io

import duckdb
import pandas as pd
import streamlit as st

csv = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""

beverages = pd.read_csv(io.StringIO(csv))

csv2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""

food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution = duckdb.sql(answer).df()

tab1, tab2 = st.tabs(["Tables", "Solution"])

with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ["Joins", "GroupBy", "Window Functions"],
        index=None,
        placeholder="Select a theme",
    )

    st.write("You selected:", option)

with tab1:
    st.write(
        """
    # SQL SRS
    Spaced Repetition System SQL practice
    """
    )

    query = st.text_input("Enter your sql query")

    st.write("The beverages table is:")
    st.dataframe(beverages)

    st.write("The food_items table is:")
    st.dataframe(food_items)

    if query:
        st.write("The entered query is:", query)
        result = duckdb.query(query).to_df()
        st.write("The queried dataframe is:", result)

    st.write("The expected output is:", solution)

with tab2:
    st.write(
        """
    # SQL SRS
    Spaced Repetition System SQL practice
    """
    )
    st.write("The solution is:", answer)
    st.dataframe(solution)
