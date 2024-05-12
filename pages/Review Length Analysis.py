
import snowflake.connector
import streamlit as st
import pandas as pd
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from os import path, getcwd
import numpy as np
from collections import Counter
st.set_page_config(
    page_title="Feedback Summary",
    page_icon=":pencil:",
    layout="wide"
   
)
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
# Streamlit app
def review_length():
    st.title("Review Length Analysis")

    # SQL query to retrieve review length and sentiment or rating
    query = """
    with review_length as (
        SELECT
            LENGTH(text) AS review_length,
             SNOWFLAKE.CORTEX.SENTIMENT(text) AS review_sentiment,
            rating AS review_rating
        FROM
            REVIEWS.AMAZON.CUSTOMERREVIEWS
    )
    select * from review_length   
    """

    # Fetch data from Snowflake
    results = fetch_data(query)

    df = pd.DataFrame(results, columns=['Review Length', 'Sentiment', 'Rating'])

    # Scatter plot of review length vs sentiment
    
    fig, ax = plt.subplots()
    ax.scatter(df['Review Length'], df['Sentiment'])
    ax.set_xlabel("Review Length")
    ax.set_ylabel("Sentiment")

    # Scatter plot of review length vs rating
    
    fig2, ax2 = plt.subplots()
    ax2.scatter(df['Review Length'], df['Rating'])
    ax2.set_xlabel("Review Length")
    ax2.set_ylabel("Rating")

    # Display both plots side by side
    col1, col2 = st.columns(2)
    with col1:
        st.write("Scatter Plot of Review Length vs Rating:")
        st.pyplot(fig)
    with col2:
        st.write(" Scatter Plot of Review Length vs Sentiment:")
        st.pyplot(fig2)

review_length()