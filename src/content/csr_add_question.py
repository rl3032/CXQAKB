import streamlit as st
from graph import get_driver
from utils.question import add_question

PRODUCT = ["All", "Permit", "Certification", "Licences", "Other"]
TECHNOLOGY = {
        "All": ["All"],
        "Permit": ["All", "Electrical", "Gas", "BPVR", "Elevating Devices", "Passenger Ropeways", "Railways", "Amusement Devices"],
        "Certification": ["All", "Electrical", "Gas", "BPVR", "Elevating Devices", "Passenger Ropeways", "Railways", "Amusement Devices"],
        "Licences": ["All", "Electrical", "Gas", "BPVR", "Elevating Devices", "Passenger Ropeways", "Railways", "Amusement Devices"],
        "Other": ["All", "Electrical", "Gas", "BPVR", "Elevating Devices", "Passenger Ropeways", "Railways", "Amusement Devices"]
    }

driver = get_driver()

st.header("Add a New Question")

# Get user name through session state
username = st.session_state.username

question = st.text_input("Enter the question")
answer = st.text_input("Enter the answer")
product = st.selectbox("Select Product", PRODUCT)
technologies = st.selectbox("Select Technology", TECHNOLOGY[product])

if st.button("Add Question"):
    technologies_list = [tech.strip() for tech in technologies.split(',')]
    with driver.session() as session:
        session.write_transaction(add_question, question, answer, product, technologies_list, username)
    st.success("Question added successfully!")
