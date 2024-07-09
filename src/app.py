import streamlit as st
import pandas as pd
from neo4j import GraphDatabase


## Function to create a connection to the Neo4j database
def create_connection():
    uri = st.secrets["NEO4J_URI"]
    user = st.secrets["NEO4J_USERNAME"]
    password = st.secrets["NEO4J_PASSWORD"]
    driver = GraphDatabase.driver(uri, auth=(user, password))
    return driver

# General function to fetch unique values for a given node label and property
def fetch_unique_values(driver, label, property_name, filters=None):
    query = f"MATCH (n:{label})"
    if filters:
        filter_clauses = []
        for key, value in filters.items():
            filter_clauses.append(f"n.{key} = '{value}'")
        query += " WHERE " + " AND ".join(filter_clauses)
    query += f" RETURN n.{property_name} AS value"
    with driver.session() as session:
        result = session.run(query)
        values = [record["value"] for record in result]
    return list(set(values))  # Remove duplicates by converting to a set and back to a list

# Function to fetch technologies
def fetch_technologies(driver):
    return fetch_unique_values(driver, "Technology", "name")

# Function to fetch services based on selected technology
def fetch_services(driver, technology):
    filters = {"technology": technology}
    return fetch_unique_values(driver, "Service", "name", filters)

# Function to fetch categories based on selected technology and service
def fetch_categories(driver, technology, service):
    filters = {"technology": technology, "service": service}
    return fetch_unique_values(driver, "Category", "name", filters)


# Function to fetch questions and answers based on selected filters
def fetch_qa(driver, technology, service, category):
    query = """
    MATCH (q:Question)-[:HAS_ANSWER]->(a:Answer)
    MATCH (q)-[:BELONGS_TO_CATEGORY]->(t:Category {name: $category, technology: $technology, service: $service})
    OPTIONAL MATCH (q) - [:HAS_FORM]->(f:Form)
    RETURN q.text AS question, a.text AS answer, a.updateTime AS `answer date`, f.name AS `form name`, f.formID AS `form id`
    """
    with driver.session() as session:
        result = session.run(query, technology=technology, service=service, category=category)
        return [{"Question": record["question"], "Answer": record["answer"], "Answer Update Date": record["answer date"], "Form Name": record["form name"], "Form ID": record["form id"]} for record in result]

# Function to fetch form questions related to a specific form
def fetch_form_questions(driver, form_id):
    query = """
    MATCH (fq:FormQuestion)<-[:HAS]-(f:Form {formID: $form_id})
    RETURN fq.text AS form_question, fq.type AS form_question_type
    """
    with driver.session() as session:
        result = session.run(query, form_id=form_id)
        return [{"Form Question": record["form_question"], "Form Question Type": record["form_question_type"]} for record in result]


# Function to fetch outdated questions and answers
def fetch_outdated_qa(driver):
    query = """
    MATCH (q:Question)-[:HAS_ANSWER]->(a:Answer)
    MATCH (q)-[:HAS_SOURCE]->(src:Source)
    WHERE datetime(a.updateTime) < datetime(src.updateTime)
    RETURN q.text AS question, a.text AS answer, 
           a.updateTime AS `answer date`, src.url AS `source url`, src.updateTime AS `source date`
    """
    with driver.session() as session:
        result = session.run(query)
        outdated_qa_pairs = [{"Question": record["question"], 
                              "Answer Update Date": record["answer date"],
                              "Source Url": record["source url"],
                              "Source Update Date": record["source date"]} for record in result]
    return outdated_qa_pairs

# Initialize counters for Q&A pairs
if "qa_counters" not in st.session_state:
    st.session_state.qa_counters = {}


# Streamlit interface
st.title("Client Experience Knowledge Base")

driver = create_connection()

# Container for outdated Q&A pairs table
outdated_qa_container = st.container()

# Fetch outdate Q&A pairs
if st.sidebar.checkbox("Check Outdated Q&A"):
    outdated_qa_pairs = fetch_outdated_qa(driver)
    
    with outdated_qa_container:
        if outdated_qa_pairs:
            st.header("Outdated Q&A")
            st.warning("There are outdated Q&A pairs that need your attention!")
            outdated_df = pd.DataFrame(outdated_qa_pairs)
            st.dataframe(outdated_df, hide_index=True)
        else:
            st.write("No outdated Q&A pairs found.")

# Step 1: Select Technology
technologies = fetch_technologies(driver)
selected_technology = st.sidebar.selectbox("Select Technology", technologies)

# Step 2: Select Service based on Technology
if selected_technology:
    services = fetch_services(driver, selected_technology)
    selected_service = st.sidebar.selectbox("Select Service", services)
else:
    selected_service = None

# Step 3: Select Category based on Technology and Service
if selected_service:
    categories = fetch_categories(driver, selected_technology, selected_service)
    selected_category = st.sidebar.selectbox("Select Category", categories)
else:
    selected_category = None

# Fetch and display Q&A pairs
if st.sidebar.button("Get Q&A") and selected_category:
    qa_pairs = fetch_qa(driver, selected_technology, selected_service, selected_category)

    for idx, qa in enumerate(qa_pairs, 1):
        st.subheader(f"Question {idx}. {qa['Question']}")
        st.write(f"**Answer Update Date**: {qa['Answer Update Date']}")
        st.write(qa["Answer"])

        # Buttons to count usage and improvements
        col1, col2, col3 = st.columns(3)
        with col1:
            count_button =  st.button("Refer to this Answer 👍", key=f"count_{idx}")
                

        with col2:
            like_button =  st.button("Like this Answer ❤️", key=f"like_{idx}")

        
        with col3:
            outdated_button = st.button("Notice Answer is outdated 🚨", key=f"notice_{idx}")
        
        # Fetch and display related form questions if the question has an associated form
        if qa["Form ID"]:
            form_questions = fetch_form_questions(driver, qa["Form ID"])
            if form_questions:
                st.write(f"**Related Form Questions for Form {qa['Form Name']} (ID: {qa['Form ID']}):**")
                for fq in form_questions:
                    st.write(f"- {fq['Form Question']} ({fq['Form Question Type']})")
driver.close()