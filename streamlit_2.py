#streamlit run streamlit_2.py

# initial_data_cleaning.py
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

def clean_trustpilot_data():
    # Your data cleaning functions
    df_trustpilot = pd.read_csv('data/data_trustpilot_clean.csv', engine='python')
    
    # All your cleaning operations
    df_trustpilot.drop(columns=['page_number'], inplace=True)
    df_trustpilot['rating'] = df_trustpilot['rating'].astype('int')
    
    # Rest of your cleaning operations...
    df_trustpilot['number_reviews'] = df_trustpilot['number_reviews'].str.replace('(?i)reviews', '', regex=True).str.strip()
    df_trustpilot['number_reviews'] = df_trustpilot['number_reviews'].str.replace('(?i)review', '', regex=True).str.strip()
    df_trustpilot['number_reviews'] = df_trustpilot['number_reviews'].astype(int)
    
    # Date conversions
    df_trustpilot['date_of_experience'] = pd.to_datetime(df_trustpilot['date_of_experience'], errors='coerce')
    df_trustpilot['date_posted'] = pd.to_datetime(df_trustpilot['date_posted'])
    
    # Handle missing values and duplicates
    df_trustpilot = df_trustpilot.drop_duplicates()
    df_trustpilot['username'] = df_trustpilot['username'].fillna('Customer')
    df_trustpilot['verification'] = df_trustpilot['verification'].fillna('Not Verified')
    df_trustpilot = df_trustpilot.dropna(axis=0, how='any', subset=['location', 'subject'])
    df_trustpilot['answer'] = df_trustpilot['answer'].fillna(0)
    
    return df_trustpilot

# app.py
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from initial_data_cleaning import clean_trustpilot_data

def main():
    st.title("Trustpilot Reviews Analysis")
    
    # Load and cache the data
    @st.cache_data
    def load_data():
        return clean_trustpilot_data()
    
    # Load the data
    try:
        df = load_data()
        st.success("Data loaded successfully!")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    pages = ["Data Overview", "Rating Analysis", "Visualizations"]
    page = st.sidebar.radio("Go to", pages)
    
    if page == "Data Overview":
        st.header("Data Overview")
        
        # Show basic dataset info
        st.subheader("Dataset Information")
        st.write(f"Number of rows: {df.shape[0]}")
        st.write(f"Number of columns: {df.shape[1]}")
        
        # Sample of the data
        st.subheader("Sample Data")
        st.dataframe(df.head())
        
    elif page == "Rating Analysis":
        st.header("Rating Analysis")
        
        # Rating statistics
        st.subheader("Rating Statistics")
        mode_value = df['rating'].mode()[0]
        mode_count = df['rating'].value_counts().iloc[0]
        median_value = df['rating'].median()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Most Common Rating", mode_value)
            st.metric("Median Rating", f"{median_value:.2f}")
        
        # Rating distribution
        st.subheader("Rating Distribution")
        rating_counts = df['rating'].value_counts().sort_index()
        st.dataframe(rating_counts)
        
    elif page == "Visualizations":
        st.header("Visualizations")
        
        # Rating distribution plot
        st.subheader("Rating Distribution Plot")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(data=df, x='rating')
        plt.title('Distribution of Ratings')
        plt.xlabel('Rating')
        plt.ylabel('Count')
        st.pyplot(fig)
        plt.close()
        
        # Additional visualizations can be added here

if __name__ == "__main__":
    main()