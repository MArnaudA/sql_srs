import duckdb
import streamlit as st


conn = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

tab1, tab2 = st.tabs(["Tables", "Solution"])

with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ["Cross Joins", "GroupBy", "Window Functions"],
        index=None,
        placeholder="Select a theme",
    )
    st.write("You selected:", option)
    exercise = conn.execute(f"SELECT * FROM memory_state WHERE theme = '{option}'").df()
    st.write(exercise)

# with tab1:
#     st.write(
#         """
#     # SQL SRS
#     Spaced Repetition System SQL practice
#     """
#     )

#     query = st.text_input("Enter your sql query")

#     st.write("The beverages table is:")
#     st.dataframe(beverages)

#     st.write("The food_items table is:")
#     st.dataframe(food_items)

#     if query:
#         st.write("The entered query is:", query)
#         result = duckdb.query(query).to_df()
#         st.write("The queried dataframe is:", result)

#     st.write("The expected output is:", solution)

# with tab2:
#     st.write(
#         """
#     # SQL SRS
#     Spaced Repetition System SQL practice
#     """
#     )
#     st.write("The solution is:", answer)
#     st.dataframe(solution)
