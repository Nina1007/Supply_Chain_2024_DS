import pandas as pd
import numpy as np
from datetime import datetime
import re

# Preparing the dataset
pd.set_option('display.max_columns', None)
df_steelseries = pd.read_csv('data/data_steelseries.csv', engine='python')

def is_valid(value, expected_type):
    if pd.isna(value):
        return False
    if expected_type == 'rating':
        return str(value) in ['1', '2', '3', '4', '5']
    elif expected_type == 'date_posted':
        if not isinstance(value, str):
            return False
        try:
            datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False
    elif expected_type == 'date_of_experience':
        if not isinstance(value, str):
            return False
        try:
            datetime.strptime(value, '%B %d, %Y')
            return True
        except ValueError:
            return False
    elif expected_type == 'location':
        return isinstance(value, str) and len(value) <= 3  # Assuming location is a country code
    elif expected_type == 'number_reviews':
        return isinstance(value, str) and 'review' in value.lower()
    return True  # For other columns, consider all values valid

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

# Apply the check to each row
df_steelseries['issues'] = df_steelseries.apply(check_row, axis=1)

# Display distribution of issues before cleaning
print("Distribution of issues before cleaning:")
issue_counts = df_steelseries['issues'].explode().value_counts()
print(issue_counts)

# Count the number of problematic rows
problematic_rows_count = df_steelseries[df_steelseries['issues'].apply(len) > 0].shape[0]
print(f"\nNumber of problematic rows: {problematic_rows_count}")

# Remove problematic rows
df_steelseries_clean = df_steelseries[df_steelseries['issues'].apply(len) == 0].copy()

# Drop the 'issues' column as it's no longer needed
df_steelseries_clean = df_steelseries_clean.drop('issues', axis=1)

print(f"\nRemoved {df_steelseries.shape[0] - df_steelseries_clean.shape[0]} rows")
print(f"Cleaned dataset now has {df_steelseries_clean.shape[0]} rows")

# Function to display unique values and their counts for a column
def display_unique_values(df, column_name):
    unique_values = df[column_name].value_counts(dropna=False)
    print(f"\nUnique values in {column_name}:")
    print(unique_values.head(10))  # Display top 10 values
    if len(unique_values) > 10:
        print(f"... (and {len(unique_values) - 10} more)")

# Check unique values in the cleaned dataset
columns_to_check = ['rating', 'location', 'number_reviews', 'verification']
for column in columns_to_check:
    display_unique_values(df_steelseries_clean, column)

# Additional checks
print("\nDataset Information:")
print(df_steelseries_clean.info())

print("\nSample of the first few rows:")
print(df_steelseries_clean.head())

print("\nSample of the last few rows:")
print(df_steelseries_clean.tail())

# Save the cleaned dataset
df_steelseries_clean.to_csv('data/data_steelseries_clean.csv', index=False)
print("Cleaned Steelseries dataset saved as 'data/data_steelseries_clean.csv'")