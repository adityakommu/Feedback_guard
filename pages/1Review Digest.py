import snowflake.connector
import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import os

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

def artic_snowflake():
    # Write directly to the app
    st.title("Feedback Summary")
    st.caption("Below visuals have been generated using Snowflake Artic")
    default_start_date = pd.to_datetime("2014-01-01")

# Use a state variable to store the selected start date
    end_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2014-01-01")   )
    start_date = st.sidebar.date_input("End Date")
    
    # Prompt for summarization
    prompt = "### Summarize this customer review in a single word. This word must be chosen from words below. Satisfied, Long-lasting, Reliable, Great, Poor Quality, Not Durable, Inconsistent, Disappointing, Do not give me long sentences, just one word from above choices ###"

    query = f"""
    WITH as1 AS (
        SELECT text, snowflake.cortex.complete('snowflake-arctic', CONCAT('\\\\\[INST\\\\\]', 
        'Summarize this customer review in a single word. This word must be chosen from words below. Satisfied, Long-lasting, Reliable, Great, Poor Quality, Not Durable, Inconsistent, Disappointing, Do not give me long sentences, just one word from above choices ###', 
        text, '\\\\\[/INST\\\\\]')) AS summary
        FROM CUSTOMERREVIEWS
        """

    # Add date filter if both start and end dates are selected
    if start_date and end_date:
        query += f"""WHERE dateadded <= '{start_date.strftime('%Y-%m-%d')}' 
                    AND dateseen >= '{end_date.strftime('%Y-%m-%d')}'"""

    query += """
        LIMIT 100
    )
    SELECT * FROM as1
    """
    


    # Fetch data from Snowflake
    results = fetch_data(query)

    # Extract summaries
    summaries = [result[1] if isinstance(result, tuple) else result for result in results]

    # Generate word cloud
    wordcloud = WordCloud(width=500, height=400, background_color='white', colormap='Set1').generate(' '.join(summaries))

    # Generate summary counts
    summary_counts = Counter(summaries)
    summary_df = pd.DataFrame.from_dict(summary_counts, orient='index', columns=['Count']).reset_index()
    summary_df = summary_df.rename(columns={'index': 'Summary'})

    # Arrange visuals side by side
    col1, col2 = st.columns(2)

    # Display word cloud in the first column
    with col1:
        st.subheader("Summary Word Cloud")
        st.image(wordcloud.to_array(), use_column_width=True)

    # Display bar graph in the second column
    with col2:
        st.subheader("Bucket Review Count")
        fig, ax = plt.subplots()
        bars = ax.bar(summary_df['Summary'], summary_df['Count'], color='darkgreen')
        ax.set_xlabel('Summary')
        ax.set_ylabel('Count')
        ax.tick_params(axis='x', labelrotation=45)  # Rotate x-axis labels
        for bar in bars:
            height = bar.get_height()
            ax.annotate('{}'.format(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        st.pyplot(fig)

artic_snowflake()
