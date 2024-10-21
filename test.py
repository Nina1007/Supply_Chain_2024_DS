import pandas as pd
import numpy as np
from datetime import datetime
import re
import csv

#Preparing the dataset
pd.set_option('display.max_columns', None)

df_flashbay = pd.read_csv('data_flashbay.csv', engine='python')

#Inspecting the data
print("Printing the first few rows: ", "\n", df_flashbay.head())

print("The dataset has ", df_flashbay.shape[1], "columns")
print("The dataset has ", df_flashbay.shape[0], "rows")

list = ['number_reviews', 'location', 'rating', 'verification']

for value in list:
    print(f"{value} has the following values", df_flashbay[value].value_counts())

for column in df_flashbay.columns:
    print(f"\nUnique values in {column}:")
    print(df_flashbay[column].value_counts(dropna=False).head())