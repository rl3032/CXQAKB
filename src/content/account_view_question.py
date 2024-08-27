
import streamlit as st
from graph import get_driver
from utils.question import get_all_qas, update_frequency, update_likes, update_outdated, mark_unverified, search_qas


PRODUCT = ["All", "Permit", "Certification", "Licences", "Other"]
TECHNOLOGY = {
        "All": ["All"],
        "Permit": ["All", "Electrical", "Gas", "BPVR", "Elevating Devices", "Passenger Ropeways", "Railways", "Amusement Devices"],
        "Certification": ["All", "Electrical", "Gas", "BPVR", "Elevating Devices", "Passenger Ropeways", "Railways", "Amusement Devices"],
        "Licences": ["All", "Electrical", "Gas", "BPVR", "Elevating Devices", "Passenger Ropeways", "Railways", "Amusement Devices"],
        "Other": ["All", "Electrical", "Gas", "BPVR", "Elevating Devices", "Passenger Ropeways", "Railways", "Amusement Devices"]
    }


driver = get_driver()


st.header("View the list of all Questions and Answers")

# Get user name through session state
username = st.session_state.username

# Search bar
search_query = st.text_input("Search Questions")


# Filters
product_col, technologies_col = st.columns(2)

with product_col:
    selected_product = st.selectbox("Select Product", PRODUCT)

with technologies_col:
    selected_technologies = st.selectbox("Select Technology", TECHNOLOGY[selected_product])


with driver.session() as session:
    qas = session.read_transaction(get_all_qas, selected_product, selected_technologies)

if search_query:
    qas = search_qas(qas, search_query)

if qas:
    for qa in qas:
        if qa['verified']:
            st.subheader(f"✅ Question: {qa['question']}")
        else:
            st.subheader(f"Question: {qa['question']}")
        st.write(f"Answer: {qa['answer']}")
        st.write(f"Last Modified: {qa['last_modified']}")
        st.write(f"Frequency: {qa['frequency']}")
        st.write(f"Likes: {qa['likes']}")
    
        refer_col, like_col, outdate_col = st.columns(3)
        
        with refer_col:
            if st.button("Refer to this Answer", key=f"refer-{qa['question']}"):
                with driver.session() as session:
                    session.write_transaction(update_frequency, qa['question'], username)
                st.success(f"Referred '{qa['question']}'")
                st.rerun()
        
        with like_col:
            if st.button("Like this Answer", key=f"like-{qa['question']}"):
                with driver.session() as session:
                    session.write_transaction(update_likes, qa['question'], username)
                st.success(f"Liked '{qa['question']}'")
                st.rerun()

        with outdate_col:
            if st.button("Notice Outdated", key=f"outdated-{qa['question']}"):
                with driver.session() as session:
                    outdated_count = session.write_transaction(update_outdated, qa['question'], username)
                    if outdated_count > 5:
                        session.write_transaction(mark_unverified, qa['question'])
                st.warning(f"Marked '{qa['question']}' as outdated")
                st.rerun()
        
else:
    st.info("No questions available.")
