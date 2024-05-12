
import snowflake.connector
import streamlit as st
import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from os import path, getcwd
import numpy as np
from collections import Counter

@st.cache_data
def fetch_data(query):
    conn = snowflake.connector.connect(
        user=st.secrets["db_username"],
        password=st.secrets["db_password"],
        account='axb13244',
        warehouse='USWEST',
        database='REVIEWS',
        schema='AMAZON',
        role='ACCOUNTADMIN'
    )
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data


def review_summary_llm():   
# Get the user's question
    
    st.write("**Below text fields are the top 5 relevant customer reviews based on your question. Output is generated on Snowflake Artic and embeddings .**")
    question = st.text_input("Please enter a question to search for relevant customer reviews.:")

    # Execute the SQL query with the user's question
    if question:
        query = f"""
        WITH ts1 AS (
            SELECT
                snowflake.cortex.EMBED_TEXT_768('e5-base-v2', text) AS similarity,
                snowflake.cortex.EMBED_TEXT_768('e5-base-v2', '{question}') AS question,
                text
            FROM REVIEWS.AMAZON.CUSTOMERREVIEWS
            LIMIT 1000
        )
        SELECT
            text,
            VECTOR_L2_DISTANCE(similarity, question)
        FROM ts1
        
        ORDER BY VECTOR_L2_DISTANCE(similarity, question) ASC
        LIMIT 5
        """
        results = fetch_data(query)
        for result in results:
            st.write(result[0])
    else:
        st.write("")
review_summary_llm()