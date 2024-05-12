import snowflake.connector
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Function to fetch data from Snowflake
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

def get_sentiment_data():
    default_start_date = pd.to_datetime("2014-01-01")

    # Use a state variable to store the selected start date
    end_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2014-01-01")   )
    start_date = st.sidebar.date_input("End Date")
    query = """
        WITH ts1 AS (
            SELECT
                text,dateadded,dateseen
            FROM REVIEWS.AMAZON.CUSTOMERREVIEWS
            
        )
        SELECT
            SNOWFLAKE.CORTEX.SENTIMENT(text) AS sentiment
        FROM ts1
        
    """
    query += f"""WHERE dateadded <= '{start_date.strftime('%Y-%m-%d')}' 
                    AND dateseen >= '{end_date.strftime('%Y-%m-%d')}' LIMIT 100"""
    
    # Fetch data from Snowflake
    results = fetch_data(query)
    
    # Extract sentiments
    sentiments = [result[0] for result in results]
    
    # Return sentiments
    #print(sentiments)
    positive_count = 0
    negative_count = 0
    for i  in sentiments:
        if i>0:
            positive_count+=1
        else:
            negative_count+=1

    
    return sentiments,positive_count,negative_count

# Function to generate sentiment distribution pie chart
def sentiment_distribution(sentiments,positive_count,negative_count):


    # Check if there are any positive or negative sentiments
    if positive_count == 0 and negative_count == 0:
        st.subheader("No Positive or Negative Sentiment Found")
    else:
        st.subheader("Sentiment Distribution:")

        # Prepare data for pie chart (only positive and negative)
        labels = ["Positive", "Negative"]
        sizes = [positive_count, negative_count]

        # Plotting pie chart (if data available)
        if any(sizes):  # Check if any values exist before plotting
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig)

def sentiment_counts_bar_chart(positive_count,negative_count):
    
    labels = ['Positive', 'Negative']  # Labels for positive and negative sentiments
    counts = [positive_count, negative_count]
    
    # Plotting bar chart
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(labels, counts, color=['green', 'red'])
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Count')
    ax.set_title('Sentiment Counts')
    st.pyplot(fig)
    
# Streamlit app
def main():
    st.title("Sentiment Analysis")
    sentiments,positive_count,negative_count = get_sentiment_data()
     # Arrange graphs side by side using columns layout
    col1, col2 = st.columns(2)
    
    # Display sentiment distribution pie chart in first column
    with col1:
        sentiment_distribution(sentiments,positive_count,negative_count)
    
    # Display sentiment counts bar chart in second column
    with col2:
        sentiment_counts_bar_chart(positive_count, negative_count)
    

# Run the Streamlit app

main()
