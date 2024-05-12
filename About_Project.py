import streamlit as st

def about_me_func():
    st.write("# Customer Feedback Review System using Snowflake-Arctic")
    st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: ##005ab3;
    }
</style>
""", unsafe_allow_html=True)
    st.markdown("""
**Team Members:**
Aditya Kommu
            
**Project Description**:
I am a passionate developer participating in the Arctic Streamlit Hackathon. Our goal is to leverage the power of Snowflake Arctic and Streamlit to create a novel AI application for analyzing Amazon customer reviews.


**Technologies Used**:

Snowflake Arctic: We chose Snowflake Arctic for its advanced analytics capabilities and seamless integration with Snowflake's data platform.

Snowflake Embeddings: We have utilized Snowflake embeddings to compare customer reviews using **COSINE SIMILARITY**, allowing us to identify similar reviews and patterns in customer feedback.

Amazon Customer Reviews Dataset: We are utilizing the extensive dataset of Amazon customer reviews to train our models and provide meaningful analysis.

**Key Features**:
- Data Preprocessing: We will clean and preprocess the Amazon customer reviews data to ensure accurate analysis and visualization.
- Sentiment Analysis: We will perform sentiment analysis on the customer reviews to extract key insights and trends. 
- Visualization: All visuals in this project have utilized **SNOWFLAKE ARTIC and CORTEX** to generate insightful visualizations. 

**Project Development**:
Throughout the hackathon, we will focus on building a robust AI application that extracts key insights from Amazon customer reviews data. Our approach involves data preprocessing, sentiment analysis, and visualization techniques using Snowflake Arctic and Cortex to deliver a comprehensive analysis of customer sentiment and product feedback.

**Why This Project**:
Customer reviews play a crucial role in understanding market trends, product performance, and customer satisfaction. By harnessing the capabilities of Snowflake Arctic and Streamlit, we aim to provide a user-friendly platform that enables businesses to gain actionable insights from Amazon customer reviews data.

***Amazon Review Dataset Location***
- [Amazon Review Dataset](https://registry.opendata.aws/amazon-reviews/)
- [Kaggle Dataset](https://www.kaggle.com/datasets/saurav9786/amazon-product-reviews/data)
                

**Connect With Us**:
- [GitHub Repository](https://github.com/adityakommu)
- [LinkedIn Profiles](https://www.linkedin.com/in/aditya-kommu-a092517b/)
    """)

                
about_me_func()
