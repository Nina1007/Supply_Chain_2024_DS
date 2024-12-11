#streamlit run streamlit.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display


st.title("Supply Chain Project Dec 2024")
st.sidebar.title("Table of contents")
pages=["Exploration", "Data Vizualization", "Modelling"]
page=st.sidebar.radio("Go to", pages)
if st.checkbox("Display"):
  st.write("Streamlit continuation")


if page == pages[0] : 
  st.write("### Presentation of data")

df_trustpilot = pd.read_csv('data/data_trustpilot_clean.csv', engine='python')
display(df_trustpilot.head())
print("These are the names of the columns present: ", "\n", df_trustpilot.columns)
print("The dataset has ", df_trustpilot.shape[1], "columns")
print("The dataset has ", df_trustpilot.shape[0], "rows")
df_trustpilot.drop(columns=['page_number'], inplace=True)
print("These are the names of the columns present: ", "\n", df_trustpilot.columns)
print("The dataset has ", df_trustpilot.shape[1], "columns")
print("The dataset has ", df_trustpilot.shape[0], "rows")
print("Printing the relevant information from the file such as type per variable: ", "n")
print(df_trustpilot.info())
print(df_trustpilot['rating'].unique())
df_trustpilot['rating'] = df_trustpilot['rating'].astype('int')
#Amending the dataset
#number_reviews: Removing 'review(s)' from cell and converting to an integer
df_trustpilot['number_reviews'] = df_trustpilot['number_reviews'].str.replace('(?i)reviews', '', regex=True).str.strip()
df_trustpilot['number_reviews'] = df_trustpilot['number_reviews'].str.replace('(?i)review', '', regex=True).str.strip()
print(df_trustpilot['number_reviews'].value_counts())
df_trustpilot['number_reviews'] = df_trustpilot['number_reviews'].astype(int)

#Verifying output
print(df_trustpilot.info())
print(df_trustpilot.head())
#date_of_experience: Converting to datetime format
df_trustpilot['date_of_experience'] = pd.to_datetime(df_trustpilot['date_of_experience'], errors='coerce')

#date_posted: convert to datetime format
df_trustpilot['date_posted'] = pd.to_datetime(df_trustpilot['date_posted'])

print(df_trustpilot.info())
print(df_trustpilot.head())
#Identifying and handling duplicates in the dataset
print("Duplicate rows before:")
print(df_trustpilot.duplicated().sum())
df_trustpilot = df_trustpilot.drop_duplicates()
print("Duplicate rows after:")
print(df_trustpilot.duplicated().sum())



if page == pages[1] : 
  st.write("### DataVizualization")

  