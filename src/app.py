import streamlit as st

if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None


role = st.session_state.role

# Login Page
login = st.Page(
    "content/account_login.py",
    title="Log in",
    icon=":material/login:"
)


# Account Pages
# Account-Page 1: Logout
logout = st.Page(
    "content/account_logout.py",
    title="Log out",
    icon=":material/logout:"
)

# Account-Page 2: View QA
view_question = st.Page(
    "content/account_view_question.py",
    title="View QAs",
    icon=":material/manage_search:"
)


# Account-Page 3: QA Data Analysis
qa_data_analysis = st.Page(
    "content/account_data_analysis.py",
    title="QA Data Report",
    icon=":material/insights:",
    default=(role == "Admin")
)

# CSR Pages

# CSR-Page 1: Add a QA pair

add_question = st.Page(
    "content/csr_add_question.py",
    title="Add Question",
    icon=":material/add_circle:",
)

# SSR Pages
## SSR-Page 1: Verify QA pairs
verify_question = st.Page(
    "content/ssr_verify_question.py",
    title="Verify QAs",
    icon=":material/healing:",
    default=(role == "SSR")
)


# Adminstrator Pages
## Admin-Page 1: User Management
admin_user_management = st.Page(
    "content/admin_user_management.py",
    title="User Management",
    icon=":material/people:"
)

# Admin-Page 2: Upload QAs
admin_upload_question = st.Page(
    "content/admin_upload_question.py",
    title="Upload QAs through CSV",
    icon=":material/file_upload:",
)


# Pages List
account_pages = [logout, view_question, qa_data_analysis]
csr_pages = [add_question]
ssr_pages = [verify_question]
admin_pages = [admin_user_management, admin_upload_question]

st.title("Knowledge Management System")
st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

page_dict = {}
if st.session_state.role in ["CSR", "SSR", "Admin"]:
    page_dict["CSR"] = csr_pages
if st.session_state.role in ["SSR", "Admin"]:
    page_dict["SSR"] = ssr_pages
if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages


if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([login])

pg.run()