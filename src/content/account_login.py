import streamlit as st
from graph import get_driver
from utils.user import authenticate_user, create_user

ROLES = [None, "SSR", "Admin"]

driver = get_driver()


st.header("Log in")
login_tab, register_tab = st.tabs(["Login", "Register"])

with login_tab:
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log in"):
        with driver.session() as session:
            user = session.write_transaction(authenticate_user, username, password)
        if user:
            st.session_state.role = user["role"]
            st.session_state.username = user["username"]
            st.rerun()
        else:
            st.error("Invalid username or password")

with register_tab:
    new_username = st.text_input("New Username", key="register_username")
    new_password = st.text_input("New Password", type="password", key="register_password")
    role = st.selectbox("Role", ["SSR", "Admin"], key="register_role")

    if st.button("Register"):
        with driver.session() as session:
            session.write_transaction(create_user, new_username, new_password, role)
        st.success(f"User '{new_username}' registered successfully!")