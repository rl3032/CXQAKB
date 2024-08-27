import streamlit as st
import pandas as pd
from graph import get_driver
from utils.question import add_question

driver = get_driver()

st.header("Upload Questions and Answers from a CSV")

# Get user name through session state
username = st.session_state.username

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    st.write(data)

    if st.button("Upload to Database"):
        with driver.session() as session:
            for index, row in data.iterrows():
                    question = row['question']
                    answer = row['answer']
                    product = row['product']
                    technologies = row['technologies']
                    session.write_transaction(add_question, question, answer, product, technologies, username)
            st.success("Questions and answers uploaded successfully!")



