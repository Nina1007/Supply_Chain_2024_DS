#streamlit run streamlit.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import numpy as np
import io
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, BaggingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
import country_converter as coco

# Performance optimization settings
st.set_page_config(page_title="Supply Chain Project Dec 2024", layout="wide")

# Cache the data loading functions
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_initial_data():
    return pd.read_csv('data/data_trustpilot_clean.csv')

@st.cache_data(ttl=3600)
def load_visualization_data():
    return pd.read_csv('data/data_trustpilot.csv.gz', encoding='utf-8')

@st.cache_data(ttl=3600)
def load_model_data():
    X_train = pd.read_csv('data/X_train.csv', index_col=0)
    X_test = pd.read_csv('data/X_test.csv', index_col=0)
    y_train = pd.read_csv('data/y_train.csv', index_col=0).squeeze()
    y_test = pd.read_csv('data/y_test.csv', index_col=0).squeeze()
    return X_train, X_test, y_train, y_test

# Main title
st.title("Supply Chain Project Dec 2024")

# Sidebar
st.sidebar.title("Table of contents")
pages = ["First Data Inspection", "Data Visualization", "Data Manipulation", "Models"]
page = st.sidebar.radio("Go to", pages)

# First Data Inspection Page
if page == "First Data Inspection":
    st.header("First Data Inspection")
    
    try:
        df = load_initial_data()
        
        # Display first 15 rows
        st.subheader("First Fifteen Rows of Dataset")
        st.dataframe(df.head(15))
        
        # Rating Analysis
        st.subheader("Rating Distribution Analysis")
        
        # Create two columns for the analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Statistical summary of ratings
            st.write("Statistical Summary of Ratings")
            rating_stats = df['rating'].describe()
            st.dataframe(rating_stats)
            
            # Detailed rating distribution
            total = len(df)
            rating_counts = df['rating'].value_counts().sort_index()
            
            st.write("Detailed Rating Distribution")
            distribution_data = []
            for rating, count in rating_counts.items():
                percentage = (count/total) * 100
                distribution_data.append({
                    "Rating": rating,
                    "Count": count,
                    "Percentage": f"{percentage:.2f}%"
                })
            st.dataframe(pd.DataFrame(distribution_data))
        
        with col2:
            # Rating distribution plot
            st.write("Rating Distribution Plot")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.countplot(data=df, x='rating')
            plt.title('Distribution of Ratings')
            plt.xlabel('Rating')
            plt.ylabel('Count')
            st.pyplot(fig)
            
            # Add conclusion about class imbalance
            st.info("**Dataset Imbalance Analysis**: The distribution plot shows a clear class imbalance in the ratings, with rating 5 being significantly more frequent than others.")
            
    except Exception as e:
        st.error(f"Error loading or processing the data: {str(e)}")

elif page == "Data Visualization":
    st.header("Data Visualization")
    
    try:
        df = load_visualization_data()
        
        # Create tabs for different visualization categories
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Text Analysis", "Rating Distributions", 
                                             "Geographic Analysis", "Company Analysis",
                                             "Correlation Analysis"])
        
        with tab1:
            st.subheader("Text Analysis Visualizations")
            
            # Word Clouds
            st.write("### Word Clouds by Rating")
            col1, col2 = st.columns(2)
            
            with col1:
                # Positive Word Cloud
                df_pos = df[df["rating"]==5]
                text = " ".join(df_pos["text_processed"].fillna("").astype(str))
                wordcloud = WordCloud(background_color="white", max_words=100,
                    width=800, height=400).generate(text)
                fig_pos = plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation="bilinear")
                plt.axis("off")
                plt.title("Word Cloud of Positive Ratings")
                st.pyplot(fig_pos)
                
            with col2:
                # Negative Word Cloud
                df_neg = df[df["rating"]==1]
                text = " ".join(df_neg["text_processed"].fillna("").astype(str))
                wordcloud = WordCloud(background_color="black", max_words=100,
                    width=800, height=400).generate(text)
                fig_neg = plt.figure(figsize=(10, 5))
                plt.imshow(wordcloud, interpolation="bilinear")
                plt.title("Word Cloud of Negative Ratings")
                plt.axis("off")
                st.pyplot(fig_neg)
            
            # Word Phrase Presence Heatmap
            st.write("### Word and Phrase Presence by Rating")
            word_list = [
                'helpful', 'excellent', 'perfect', 'amazing', 'great', 'fantastic',
                'recommend', 'best', 'love', 'wonderful', 'satisfied', 'pleased',
                'unhelpful', 'terrible', 'awful', 'horrible', 'poor', 'disappointing',
                'avoid', 'worst', 'never', 'waste', 'annoying', 'frustrating',
                'great service', 'poor quality','great product', 'not working', 'reliable', 
                'great experience', 'bad experience', 'still waiting', 
                'immediately', 'delayed', 'always', 'never', 'sometimes', 'usually',
                'first time', 'never again','highly recommend'
            ]
            
            # Calculate word presence percentages
            result_df = pd.DataFrame()
            for word in word_list:
                grouped = df.groupby('rating')['text_processed'].apply(
                    lambda x: (x.astype(str).str.contains(word, case=False, na=False) * 100).mean()
                ).round(0)
                result_df[word] = grouped
            
            fig_heatmap = plt.figure(figsize=(12, 8))
            sns.heatmap(result_df.T, annot=True, cmap="YlGnBu", fmt='g')
            plt.xlabel("Rating")
            plt.ylabel("Words and Phrases")
            plt.title("Percent of Word and Phrase Presence by Rating")
            st.pyplot(fig_heatmap)
            
            # Word Count Distribution
            st.write("### Word Count Distribution by Rating")
            fig_wordcount = plt.figure(figsize=(10, 6))
            sns.boxplot(x='rating', y='text_word_length', data=df)
            plt.title('Word Count Distribution by Rating')
            plt.xlabel('Rating')
            plt.ylabel('Number of Words')
            st.pyplot(fig_wordcount)
            
        with tab2:
            st.subheader("Rating Distribution Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Rating by Repeat Reviewer
                st.write("### Rating Distribution by Reviewer Type")
                fig_repeat = plt.figure(figsize=(10, 6))
                sns.boxplot(x='repeat_reviewer', y='rating', data=df)
                plt.title('Rating Distribution by Reviewer Type')
                plt.xlabel('Reviewer Type')
                plt.ylabel('Rating')
                st.pyplot(fig_repeat)
            
            with col2:
                # Rating by Review Time
                st.write("### Rating Distribution by Review Time")
                fig_time = plt.figure(figsize=(10, 6))
                sns.boxplot(x='review_time', y='rating', data=df)
                plt.title('Rating Distribution by Review Time')
                plt.xlabel('Review Time')
                plt.ylabel('Rating')
                st.pyplot(fig_time)
            
            # Rating Distribution by Time of Day
            st.write("### Rating Distribution by Time of Day")
            time_day_counts = df.groupby(['time_of_day', 'rating']).size().unstack(fill_value=0)
            fig_timeday = plt.figure(figsize=(12, 6))
            sns.heatmap(time_day_counts, annot=True, fmt='d', cmap='YlOrRd')
            plt.title('Number of Reviews by Time of Day and Rating')
            plt.xlabel('Rating')
            plt.ylabel('Time of Day')
            st.pyplot(fig_timeday)
            
        with tab3:
            st.subheader("Geographic Analysis")
            
            # Rating Distribution by Top 10 Countries
            top_countries = df['location'].value_counts().nlargest(10).index
            df_top_countries = df[df['location'].isin(top_countries)]
            
            st.write("### Rating Distribution by Top 10 Countries")
            fig_countries = plt.figure(figsize=(12, 6))
            sns.boxplot(x='location', y='rating', data=df_top_countries)
            plt.xticks(rotation=45)
            plt.title('Rating Distribution by Top 10 Countries')
            st.pyplot(fig_countries)
            
            # Choropleth Plot
            st.write("### Global Rating Distribution")
            country_ratings = df.groupby('location')['rating'].mean().reset_index()
            cc = coco.CountryConverter()
            country_ratings['location_iso3'] = cc.convert(country_ratings['location'].tolist(), to='ISO3')
            
            fig_choropleth = px.choropleth(
                country_ratings,
                locations='location_iso3',
                color='rating',
                color_continuous_scale="RdYlGn",
                range_color=(1, 5),
                title='Average Ratings by Country'
            )
            
            fig_choropleth.update_layout(
                margin={"r":0,"t":30,"l":0,"b":0},
                title_x=0.5,
                height=600,
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    projection_type='equirectangular'
                )
            )
            
            st.plotly_chart(fig_choropleth)
            
        with tab4:
            st.subheader("Company Analysis")
            
            # Rating Distribution by Company
            top_companies = df['company'].value_counts().nlargest(10).index
            df_top_companies = df[df['company'].isin(top_companies)]
            
            st.write("### Rating Distribution by Top 10 Companies")
            fig_companies = plt.figure(figsize=(12, 6))
            sns.boxplot(x='company', y='rating', data=df_top_companies)
            plt.xticks(rotation=45, ha='right')
            plt.title('Rating Distribution by Top 10 Companies')
            st.pyplot(fig_companies)

        with tab5:
            st.subheader("Correlation Analysis")
            
            # Heatmap of numeric variables
            st.write("### Correlation Heatmap of Numeric Variables")
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
            correlation_matrix = df[numeric_cols].corr()
            
            fig_heatmap = plt.figure(figsize=(20, 16))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
            plt.title('Correlation Heatmap of Numeric Variables')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig_heatmap)
            
    except Exception as e:
        st.error(f"Error loading or processing the data: {str(e)}")

elif page == "Data Manipulation":
    st.header("Data Manipulation")
    
    try:
        # Initial Dataset section
        st.write("## Initial Dataset")
        initial_df = pd.read_csv('data/train_post_cluster_full.csv')
        st.dataframe(initial_df.head())
        
        # Selected Features section
        st.write("## Selected Features")
        selected_df = pd.read_csv('data/X_train.csv')
        if 'Unnamed: 0' in selected_df.columns:
            selected_df = selected_df.drop('Unnamed: 0', axis=1)
        st.dataframe(selected_df.head())
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")

elif page == "Models":
    st.header("Model Performance Analysis")
    
    try:
        X_train, X_test, y_train, y_test = load_model_data()
        
        if X_train is not None:
            tab1, tab2, tab3 = st.tabs(["Gradient Boosting with SMOTE", 
                                       "Random Forest Bagging with RUS",
                                       "SVC with RUS"])
            
            with tab1:
                st.subheader("Gradient Boosting with SMOTE Sampling")
                
                if st.button("Train Gradient Boosting Model", key="gb_button"):
                    with st.spinner("Training model..."):
                        scaler = StandardScaler()
                        X_train_scaled = scaler.fit_transform(X_train)
                        X_test_scaled = scaler.transform(X_test)
                        
                        smote = SMOTE(random_state=25)
                        X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)
                        
                        gb = GradientBoostingClassifier(random_state=25, n_estimators=20)
                        gb.fit(X_train_smote, y_train_smote)
                        
                        y_pred = gb.predict(X_test_scaled)
                        
                        accuracy = accuracy_score(y_test, y_pred)
                        f1_weighted = f1_score(y_test, y_pred, average='weighted')
                        f1_per_class = f1_score(y_test, y_pred, average=None)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Accuracy", f"{accuracy:.4f}")
                            st.metric("Weighted F1 Score", f"{f1_weighted:.4f}")
                        
                        with col2:
                            cm = confusion_matrix(y_test, y_pred)
                            fig, ax = plt.subplots(figsize=(8, 6))
                            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
                            plt.title('Confusion Matrix')
                            plt.xlabel('Predicted')
                            plt.ylabel('True')
                            st.pyplot(fig)
                        
                        st.write("F1 Scores per Class:")
                        f1_df = pd.DataFrame({
                            'Class': range(1, len(f1_per_class) + 1),
                            'F1 Score': f1_per_class
                        })
                        st.table(f1_df)
            
            with tab2:
                st.subheader("Random Forest Bagging with RUS Sampling")
                
                if st.button("Train Random Forest Bagging Model", key="rf_button"):
                    with st.spinner("Training model..."):
                        scaler = StandardScaler()
                        X_train_scaled = scaler.fit_transform(X_train)
                        X_test_scaled = scaler.transform(X_test)
                        
                        rus = RandomUnderSampler(random_state=25)
                        X_train_rus, y_train_rus = rus.fit_resample(X_train_scaled, y_train)
                        
                        rf = RandomForestClassifier(random_state=25, n_estimators=20)
                        rf_bagging = BaggingClassifier(
                            estimator=rf,
                            n_estimators=10,
                            random_state=25
                        )
                        rf_bagging.fit(X_train_rus, y_train_rus)
                        
                        y_pred = rf_bagging.predict(X_test_scaled)
                        
                        accuracy = accuracy_score(y_test, y_pred)
                        f1_weighted = f1_score(y_test, y_pred, average='weighted')
                        f1_per_class = f1_score(y_test, y_pred, average=None)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Accuracy", f"{accuracy:.4f}")
                            st.metric("Weighted F1 Score", f"{f1_weighted:.4f}")
                        
                        with col2:
                            cm = confusion_matrix(y_test, y_pred)
                            fig, ax = plt.subplots(figsize=(8, 6))
                            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
                            plt.title('Confusion Matrix')
                            plt.xlabel('Predicted')
                            plt.ylabel('True')
                            st.pyplot(fig)
                        
                        st.write("F1 Scores per Class:")
                        f1_df = pd.DataFrame({
                            'Class': range(1, len(f1_per_class) + 1),
                            'F1 Score': f1_per_class
                        })
                        st.table(f1_df)
            
            with tab3:
                st.subheader("SVC with RUS Sampling")
                
                if st.button("Train SVC Model", key="svc_button"):
                    with st.spinner("Training model..."):
                        scaler = StandardScaler()
                        X_train_scaled = scaler.fit_transform(X_train)
                        X_test_scaled = scaler.transform(X_test)
                        
                        rus = RandomUnderSampler(random_state=25)
                        X_train_rus, y_train_rus = rus.fit_resample(X_train_scaled, y_train)
                        
                        svc = SVC(random_state=25)
                        svc.fit(X_train_rus, y_train_rus)
                        
                        y_pred = svc.predict(X_test_scaled)
                        
                        accuracy = accuracy_score(y_test, y_pred)
                        f1_weighted = f1_score(y_test, y_pred, average='weighted')
                        f1_per_class = f1_score(y_test, y_pred, average=None)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Accuracy", f"{accuracy:.4f}")
                            st.metric("Weighted F1 Score", f"{f1_weighted:.4f}")
                        
                        with col2:
                            cm = confusion_matrix(y_test, y_pred)
                            fig, ax = plt.subplots(figsize=(8, 6))
                            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
                            plt.title('Confusion Matrix')
                            plt.xlabel('Predicted')
                            plt.ylabel('True')
                            st.pyplot(fig)
                        
                        st.write("F1 Scores per Class:")
                        f1_df = pd.DataFrame({
                            'Class': range(1, len(f1_per_class) + 1),
                            'F1 Score': f1_per_class
                        })
                        st.table(f1_df)
                        
    except Exception as e:
        st.error(f"Error loading or processing the data: {str(e)}")