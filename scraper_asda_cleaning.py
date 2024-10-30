import pandas as pd
import numpy as np
from datetime import datetime
import re
import os

pd.set_option('display.max_columns', None)
df_asda = pd.read_csv('data/data_asda.csv', engine='python')

def is_valid(value, expected_type):
    if pd.isna(value):
        return False
    
    if expected_type == 'rating':
        try:
            rating = float(str(value).strip())
            return rating in [1.0, 2.0, 3.0, 4.0, 5.0]
        except ValueError:
            return False
            
    elif expected_type == 'date_posted':
        if not isinstance(value, str):
            return False
        try:
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                try:
                    datetime.strptime(value, fmt)
                    return True
                except ValueError:
                    continue
            return False
        except Exception:
            return False
            
    elif expected_type == 'date_of_experience':
        if not isinstance(value, str):
            return False
        try:
            for fmt in ['%B %d, %Y', '%Y-%m-%d', '%d/%m/%Y']:
                try:
                    datetime.strptime(value, fmt)
                    return True
                except ValueError:
                    continue
            return False
        except Exception:
            return False
            
    elif expected_type == 'location':
        return isinstance(value, str) and len(value.strip()) > 0
        
    elif expected_type == 'number_reviews':
        try:
            num = re.findall(r'\d+', str(value))
            return len(num) > 0
        except Exception:
            return False
            
    return True

def check_row(row):
    issues = []
    if not is_valid(row['rating'], 'rating'):
        issues.append('rating')
    if not is_valid(row['date_posted'], 'date_posted'):
        issues.append('date_posted')
    if not is_valid(row['date_of_experience'], 'date_of_experience'):
        issues.append('date_of_experience')
    if not is_valid(row['location'], 'location'):
        issues.append('location')
    if not is_valid(row['number_reviews'], 'number_reviews'):
        issues.append('number_reviews')
    return issues

def analyze_column(df, column_name):
    print(f"Analyzing {column_name}:")
    print("Sample unique values:")
    print(df[column_name].unique()[:5])
    print(f"Data type: {df[column_name].dtype}")
    print(f"Null values: {df[column_name].isna().sum()}")

columns_to_check = ['rating', 'date_posted', 'date_of_experience', 'location', 'number_reviews']
for col in columns_to_check:
    analyze_column(df_asda, col)

df_asda['issues'] = df_asda.apply(check_row, axis=1)

print("Distribution of issues after updating validation:")
issue_counts = df_asda['issues'].explode().value_counts()
print(issue_counts)

df_asda_clean = df_asda[df_asda['issues'].apply(len) == 0].copy()
df_asda_clean = df_asda_clean.drop('issues', axis=1)

print(f"Original dataset size: {df_asda.shape[0]}")
print(f"Cleaned dataset size: {df_asda_clean.shape[0]}")
print(f"Removed {df_asda.shape[0] - df_asda_clean.shape[0]} rows")

if df_asda_clean.shape[0] > df_asda.shape[0] * 0.5:  
    df_asda_clean.to_csv('data/data_asda_clean.csv', index=False)
    print("Cleaned dataset saved successfully")
else:
    print("Warning: Too many rows would be removed. Please check the validation criteria.")