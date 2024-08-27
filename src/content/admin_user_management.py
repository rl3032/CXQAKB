import streamlit as st
from graph import get_driver
from utils.user import create_user, delete_user, update_password

driver = get_driver()

st.header("Manage Users")

option = st.selectbox("Select an option", ["Add User", "Remove User", "Update Password"])

if option == "Add User":
    st.subheader("Add User")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["CSR", "SSR", "Admin"])
    if st.button("Add User"):
        with driver.session() as session:
            session.write_transaction(create_user, username, password, role)
        st.success(f"User '{username}' added successfully!")

elif option == "Remove User":
    st.subheader("Remove User")
    username = st.text_input("Username")
    if st.button("Remove User"):
        with driver.session() as session:
            session.write_transaction(delete_user, username)
        st.success(f"User '{username}' removed successfully!")

elif option == "Update Password":
    st.subheader("Update Password")
    username = st.text_input("Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Update Password"):
        with driver.session() as session:
            session.write_transaction(update_password, username, new_password)
        st.success(f"Password for '{username}' updated successfully!")