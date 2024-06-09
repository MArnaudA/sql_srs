import streamlit as st
import pandas as pd
import duckdb

st.write("""
# SQL SRS
Spaced Repetition System SQL practice
""")
with st.sidebar:
    option = st.selectbox(
        "What would you like to review?"
        , ["Joins", "GroupBy", "Window Functions"],
        index=None,
        placeholder='Select a theme'
    )

    st.write('You selected:', option)

query = st.text_input('Enter your sql query')

df = pd.DataFrame({
    'col1': [1, 2, 3, 4],
    'col2': [5, 6, 7, 8]
})

st.write('Please note that table name is df')
st.write('The entered query is:', query)

st.write('The initial dataframe is:')
st.dataframe(df)


queried_df = duckdb.query(query).to_df()

st.write('The queried dataframe is:', queried_df)



