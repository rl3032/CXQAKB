import streamlit as st
from graph import get_driver
from utils.question import get_unverified_qas, update_question, verify_question, remove_question

PRODUCT = ["All", "Permit", "Certification", "Licences", "Other"]
TECHNOLOGY = {
        "All": ["All"],
        "Permit": ["All", "Electrical", "Gas", "BPVR", "Elevating Devices", "Passenger Ropeways", "Railways", "Amusement Devices"],
        "Certification": ["All", "Electrical", "Gas", "BPVR", "Elevating Devices", "Passenger Ropeways", "Railways", "Amusement Devices"],
        "Licences": ["All", "Electrical", "Gas", "BPVR", "Elevating Devices", "Passenger Ropeways", "Railways", "Amusement Devices"],
        "Other": ["All", "Electrical", "Gas", "BPVR", "Elevating Devices", "Passenger Ropeways", "Railways", "Amusement Devices"]
    }

driver = get_driver()

st.header('Verify Questions and Answers')

# Get user name through session state
username = st.session_state.username

# Filters
product_col, technologies_col = st.columns(2)

with product_col:
    selected_product = st.selectbox("Select Product", PRODUCT)

with technologies_col:
    selected_technologies = st.selectbox("Select Technology", TECHNOLOGY[selected_product])

with driver.session() as session:
    unverified_qas = session.read_transaction(get_unverified_qas, selected_product, selected_technologies)

if unverified_qas:
    for qa in unverified_qas:
        st.subheader(f"Question: {qa['question']}")
        new_question = st.text_input("Edit Question", qa['question'], key=f"question-{qa['question']}")
        new_answer = st.text_area("Edit Answer", qa['answer'], key=f"answer-{qa['question']}")
        
        save_col, verify_col, remove_col = st.columns(3)
        with save_col:
            if st.button(f"Save QA", key=f"save-{qa['question']}"):
                with driver.session() as session:
                    session.write_transaction(update_question, qa['question'], new_question, new_answer, username)
                st.success(f"Question '{qa['question']}' has been updated!")
                st.rerun()

        with verify_col:
            if st.button(f"Verify QA", key=f"verify-{qa['question']}"):
                with driver.session() as session:
                    session.write_transaction(verify_question, qa['question'], username)
                st.success(f"Question '{qa['question']}' has been verified!")
                st.rerun()
        
        with remove_col:
            if st.button(f"Remove QA", key=f"remove-{qa['question']}"):
                with driver.session() as session:
                    session.write_transaction(remove_question, qa['question'])
                st.success(f"Question '{qa['question']}' has been removed!")
                st.rerun()
else:
    st.info("No unverified questions available.")