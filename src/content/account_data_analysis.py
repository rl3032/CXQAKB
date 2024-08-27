import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from graph import get_driver
from utils.question import get_all_qas

driver = get_driver()

st.header("Data Analysis of QAs")

with driver.session() as session:
    qas = session.read_transaction(get_all_qas, "All", "All")

if qas:
    df = pd.DataFrame(qas)

    st.subheader("QAs by Verification Status")
    verified_counts = df['verified'].value_counts()
    st.bar_chart(verified_counts)


    st.subheader("QAs by Frequency")
    fig, ax = plt.subplots()
    df['frequency'].plot(kind='hist', bins=20, ax=ax)
    ax.set_title("Distribution of QA Frequency")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Number of QAs")
    st.pyplot(fig)
else:
    st.warning("No QA data available.")





