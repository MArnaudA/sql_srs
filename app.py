import os
import logging

import duckdb
import streamlit as st

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("Creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("data/init_db.py").read())

conn = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ["Cross Joins", "GroupBy", "Window Functions"],
        index=None,
        placeholder="Select a theme",
    )
    if option:
        exercises = conn.execute(
            f"SELECT * FROM memory_state WHERE theme = '{option}'"
        ).df()
        st.write(exercises)
        exercise_name = exercises["exercise_name"][0]
        with open(f"solutions/{exercise_name}.sql", "r") as file:
            solution_query = file.read()
        solution_df = conn.execute(solution_query).df()

st.write(
    """
    # SQL SRS
    Spaced Repetition System SQL practice
    """
)

query = st.text_input("Enter your sql query")

tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:

    if option:
        for table in exercises["tables"][0]:
            df = conn.execute(f"SELECT * FROM {table}").df()
            st.write(f"The {table} table is:")
            st.dataframe(df)

    else:
        st.write("Choose a theme to review")

    if query:
        result = conn.execute(query).df()
        st.write("The queried dataframe is:", result)

        if result.shape[0] != solution_df.shape[0]:
            st.write("The number of rows is incorrect")
        elif result.shape[1] != solution_df.shape[1]:
            st.write("The number of columns is incorrect")
        elif not result.compare(solution_df).empty:
            st.write("The content is incorrect")
        else:
            st.write("The query is correct !")

    if option:
        st.write("The expected output is:")
        st.dataframe(solution_df)

with tab2:
    if option:
        if query:
            result = conn.execute(query).df()
            st.write("The queried dataframe is:", result)
        st.write("The solution is:", solution_query)
        st.dataframe(solution_df)
