import ast

import duckdb
import streamlit as st


conn = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ["Cross Joins", "GroupBy", "Window Functions"],
        index=None,
        placeholder="Select a theme",
    )
    if option:
        exercise = conn.execute(f"SELECT * FROM memory_state WHERE theme = '{option}'").df()
        st.write(exercise)

tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:
    st.write(
        """
    # SQL SRS
    Spaced Repetition System SQL practice
    """
    )
    if option:
        for table in exercise["tables"][0]:
            df = conn.execute(f"SELECT * FROM {table}").df()
            st.write(f"The {table} table is:")
            st.dataframe(df)

    else:
        st.write("Choose a theme to review")
    
    query = st.text_input("Enter your sql query")

    if query:
        result = conn.execute(query).df()
        st.write("The queried dataframe is:", result)

    # st.write("The expected output is:", solution)

# with tab2:
#     st.write(
#         """
#     # SQL SRS
#     Spaced Repetition System SQL practice
#     """
#     )
#     st.write("The solution is:", answer)
#     st.dataframe(solution)
