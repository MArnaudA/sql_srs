import logging
import os

import duckdb
import streamlit as st
from datetime import date, timedelta

# Create the data folder if it does not exist

if "data" not in os.listdir():
    logging.error(os.listdir())
    logging.error("Creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("data/init_db.py").read())

# ------------- Defined functions -------------


def get_tables(conn, exercises):
    """
    Display tables of the selected exercise

    Parameters:
        conn (duckdb.Connection): The duckdb connection object.
        exercises (pandas.DataFrame): The exercises dataframe.

    Returns:
        None
    """
    for table in exercises["tables"][0]:
        df = conn.execute(f"SELECT * FROM {table}").df()
        st.write(f"The {table} table is:")
        st.dataframe(df)


def get_selected_theme(conn):
    """
    Retrieves the selected theme from the database among themes with exercises.

    Parameters:
        conn: The database connection object.

    Returns:
        option: The selected theme.

    """
    list_unique_themes = conn.execute("SELECT DISTINCT theme FROM memory_state").df()
    option = st.selectbox(
        "What would you like to review?",
        list_unique_themes["theme"].tolist(),
        index=None,
        placeholder="Select a theme",
    )
    return option


def show_exercise(conn, option):
    """
    Retrieves exercise from the database based on the specified theme.

    Parameters:
        conn (Connection): The database connection object.
        option (str): The theme of the exercises to retrieve.

    Returns:
        DataFrame: A DataFrame containing the retrieved exercises.
    """
    exercises = conn.execute(
        f"""SELECT * FROM memory_state 
                WHERE theme = '{option}' ORDER BY last_reviewed
                """
    ).df()
    question = exercises["question"][0]
    return exercises, question


def show_exercise_no_option(conn):
    """
    Retrieves all exercises from database.

    Parameters:
        conn (Connection): The database connection object.

    Returns:
        None
    """
    exercise = conn.execute("SELECT * FROM memory_state ORDER BY last_reviewed").df()
    question = exercise["question"][0]
    return exercise, question


def get_exercise_solution(conn, exercise_name):
    """
    Retrieves the solution query and result dataframe for a given exercise.

    Parameters:
        conn (connection): The database connection object.
        exercise_name (str): The name of the exercise.

    Returns:
        tuple: A tuple containing the solution query (str) and the result dataframe (pandas.DataFrame).
    """
    with open(f"solutions/{exercise_name}.sql", "r") as file:
        solution_query = file.read()
    solution_df = conn.execute(solution_query).df()
    return solution_query, solution_df


def verify_query(conn, solution_df, query):
    """
    Verifies the correctness of the query.

    Verify the correctness of the query by comparing the result of the query with the expected result.
    First, the function executes the query and retrieves the result dataframe.
    Then, it compares the number of rows and columns and the content of the result with the expected result.

    Parameters:
        conn (Connection): The database connection object.
        solution_df (DataFrame): The expected result dataframe.
        query (str): The query to verify.

    Returns:
        None
    """

    try:
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

    except (AttributeError, duckdb.ParserException) as e:
        st.write("Oops! There is a syntax error in your query. Please try again.")
        result = None

def button_next_review(conn, exercise_name):
    for n_days in [2,7,21]:
        if st.button(f"Review in {n_days} days"):
            next_review = date.today() + timedelta(days=n_days)
            conn.execute(
                f"""UPDATE memory_state SET last_reviewed = '{next_review}' 
                WHERE exercise_name = '{exercise_name}'"""
            )
            st.write(f"Review scheduled in {n_days} days")
    
    if st.button("Reset all review dates"):
        conn.execute(
            f"""UPDATE memory_state SET last_reviewed = '2021-09-01'"""
        )
        st.write("Review date reset")
    
    if st.button("Show review dates"):
        if "button_show_review_dates" not in st.session_state:
            st.session_state.button_show_review_dates = True
        else:
            if st.session_state.button_show_review_dates:
                st.session_state.button_show_review_dates = False
            else:
                st.session_state.button_show_review_dates = True
        if st.session_state.button_show_review_dates:
            review_dates = conn.execute("SELECT exercise_name, last_reviewed FROM memory_state").df()
            st.write(review_dates)



# ------------- Streamlit app -------------

conn = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    option = get_selected_theme(conn)
    if option:
        # show exercises among the selected theme
        exercises, question = show_exercise(conn, option)
    else:
        # show oldest reviewed exercise among all exercises
        exercises, question = show_exercise_no_option(conn)
    exercise_name = exercises["exercise_name"][0]
    solution_query, solution_df = get_exercise_solution(conn, exercise_name)

st.write(
    """
    # SQL SRS
    Spaced Repetition System SQL practice
    """
)

query = st.text_input("Enter your sql query")

tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:

    st.write("Question : ", question)
    get_tables(conn, exercises)

    if query:
        verify_query(conn, solution_df, query)

    st.write("The expected output is:")
    st.dataframe(solution_df)

with tab2:
    if query:
        verify_query(conn, solution_df, query)
    st.write("The solution is:", solution_query)
    st.dataframe(solution_df)
