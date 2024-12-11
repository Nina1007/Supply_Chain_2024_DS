# %%
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import seaborn as sns

from datetime import datetime
from IPython.display import display

# %%
#Preparing the dataset
pd.set_option('display.max_rows', None) 
pd.set_option('display.max_columns', None)

df_trustpilot = pd.read_csv('data/data_trustpilot_clean.csv', engine='python')


# %%
display(df_trustpilot.head())

# %% [markdown]
# STAGE 1 - DATASET INSPECTIONS

# %%
#Inspecting the full dataset

print("These are the names of the columns present: ", "\n", df_trustpilot.columns)
print("The dataset has ", df_trustpilot.shape[1], "columns")
print("The dataset has ", df_trustpilot.shape[0], "rows")

# %%
#Deleting the page_number column as it is no longer needed or relevant
df_trustpilot.drop(columns=['page_number'], inplace=True)

#Verifying the output
print("These are the names of the columns present: ", "\n", df_trustpilot.columns)
print("The dataset has ", df_trustpilot.shape[1], "columns")
print("The dataset has ", df_trustpilot.shape[0], "rows")

# %%
print("Printing the relevant information from the file such as type per variable: ", "n")
print(df_trustpilot.info())

# %%
#Converting rating to integer
print(df_trustpilot['rating'].unique())
df_trustpilot['rating'] = df_trustpilot['rating'].astype('int')

# %%
#Amending the dataset
#number_reviews: Removing 'review(s)' from cell and converting to an integer
df_trustpilot['number_reviews'] = df_trustpilot['number_reviews'].str.replace('(?i)reviews', '', regex=True).str.strip()
df_trustpilot['number_reviews'] = df_trustpilot['number_reviews'].str.replace('(?i)review', '', regex=True).str.strip()
print(df_trustpilot['number_reviews'].value_counts())
df_trustpilot['number_reviews'] = df_trustpilot['number_reviews'].astype(int)

#Verifying output
print(df_trustpilot.info())
print(df_trustpilot.head())

# %%
#date_of_experience: Converting to datetime format
df_trustpilot['date_of_experience'] = pd.to_datetime(df_trustpilot['date_of_experience'], errors='coerce')

#date_posted: convert to datetime format
df_trustpilot['date_posted'] = pd.to_datetime(df_trustpilot['date_posted'])

print(df_trustpilot.info())
print(df_trustpilot.head())

# %% [markdown]
# STAGE 2 - DUPLICATES AND MISSING VALUES

# %%
#Identifying and handling duplicates in the dataset
print("Duplicate rows before:")
print(df_trustpilot.duplicated().sum())
df_trustpilot = df_trustpilot.drop_duplicates()
print("Duplicate rows after:")
print(df_trustpilot.duplicated().sum())

# %%
#Identifying missing values in the dataset
print("Missing values:")
print(df_trustpilot.isnull().sum())

# %%
#Handling missing values

#Username missing value
print("This is the distribution of the types of username in the dataset: ", "\n", df_trustpilot['username'].value_counts().head())

#The username with the highest number in the dataset is 'Customer'. As this is a non-descript name for a username, we will apply it to the missing username.
df_trustpilot['username'] = df_trustpilot['username'].fillna('Customer')

#Verification missing value
print("This is the distribution of the types of verifications in the dataset: ", "\n", df_trustpilot['verification'].value_counts().head())

#Inspection indicates that there is no value under verification specifically indicating that a user is not verified. We will hence create a new variable named 'Not Verified' and fill the n/a values with it. 
df_trustpilot['verification'] = df_trustpilot['verification'].fillna('Not Verified')

#Subject and location with missing values will be dropped due to the low number
df_trustpilot = df_trustpilot.dropna(axis=0, how='any', subset=['location', 'subject'])

# Answer has a large number of empty values, which is to be expected.
# We will fill those values with 0
df_trustpilot['answer'] = df_trustpilot['answer'].fillna(0)

df_trustpilot.dropna(inplace=True)

print("Missing values:")
print(df_trustpilot.isnull().sum())

print("The dataset has ", df_trustpilot.shape[1], "columns")
print("The dataset has ", df_trustpilot.shape[0], "rows")


# %%
print("Checking dtypes are correct:")
print(df_trustpilot.info())

print("Verifying there are no more missing values:")
print(df_trustpilot.isnull().sum().sum())

print("Verifying there are no more duplicates:")
print(df_trustpilot.duplicated().sum())


# %%
#Fix content standardization
print(df_trustpilot.columns)

#username
display(df_trustpilot['username'].value_counts().head(10))
#Standardizing 'customer' and 'Customer'
df_trustpilot['username'] = df_trustpilot['username'].str.title()

#There are additional entries that are not of value to us in this column. 'Quicken Member' and 'Anonymous' should also be converted to 'Customer' as all of these entries are people who did not provide their real name.
replacements = {'Quicken Member': 'Customer','Anonymous': 'Customer', 'Anounymous': 'Customer'}
df_trustpilot['username'] = df_trustpilot['username'].replace(replacements)
display(df_trustpilot['username'].value_counts().head(10))

# %% [markdown]
# STAGE 3 - TARGET VARIABLE INSPECTION

# %%
#Inspecting statistical distributions of target variable 'rating'
print("These are the statistical distributions of the target variable present in the dataset: ", "\n")
print(df_trustpilot['rating'].describe())

#Calculating mode, mean and median for each numeric variable
mode_value = df_trustpilot['rating'].mode()[0]
mode_count = df_trustpilot['rating'].value_counts().iloc[0]
median_value = df_trustpilot['rating'].median()
    
print(f"The most common rating is {mode_value}, appearing {mode_count} times")
print(f"The median rating is: {median_value:.2f}")

# %%
#Shows the distribution of rating
plt.figure(figsize=(4, 4))
sns.countplot(data=df_trustpilot, x='rating')
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.show()

#Distribution shows a class imbalance

# %%
#Rating imbalance analysis
total = len(df_trustpilot)
rating_counts = df_trustpilot['rating'].value_counts().sort_index()
print("\nDetailed class distribution:")
for rating, count in rating_counts.items():
    percentage = (count/total) * 100
    ratio_to_max = count/rating_counts.max()
    print(f"Rating {rating}:")
    print(f"  Count: {count}")
    print(f"  Percentage: {percentage:.2f}%")
    print(f"  Ratio to largest class: 1:{1/ratio_to_max:.2f}")

# %%
#Inspecting final output 

print(df_trustpilot.columns)
print(df_trustpilot.info())
print("The Trustpilot dataset has ", df_trustpilot.shape[1], "columns")
print("The Trustpilot dataset has ", df_trustpilot.shape[0], "rows")
display(df_trustpilot.head())

# %%
import os

os.makedirs('data', exist_ok=True)

csv_path = 'data/data_trustpilot_first.csv'
df_trustpilot.to_csv(csv_path, index=False)
print(f"DataFrame exported to {csv_path}")

# %% [markdown]
# 


