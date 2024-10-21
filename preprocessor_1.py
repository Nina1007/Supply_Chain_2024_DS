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
print("Printing the last few rows: ", "\n", df_flashbay.tail())

print("Printing the relevant information from the file such as type per variable: ", "\n")
print(df_flashbay.info())
print("This is the distribution of the types of variables in the dataset: ", "\n", df_flashbay.dtypes.value_counts())

print("These are the names of the columns present: ", "\n", df_flashbay.columns)
print("The dataset has ", df_flashbay.shape[1], "columns")
print("The dataset has ", df_flashbay.shape[0], "rows")

#Amending the dataset
#number_reviews: Removing 'review(s)' from cell and converting to an integer
df_flashbay['number_reviews'] = df_flashbay['number_reviews'].str.replace('(?i)reviews', '', regex=True).str.strip()
df_flashbay['number_reviews'] = df_flashbay['number_reviews'].str.replace('(?i)review', '', regex=True).str.strip()
print(df_flashbay['number_reviews'].value_counts())
df_flashbay['number_reviews'] = df_flashbay['number_reviews'].astype(int)
print(df_flashbay.info())

#date_of_experience: Converting to datetime format
df_flashbay['date_of_experience'] = pd.to_datetime(df_flashbay['date_of_experience'], errors='coerce')
print(df_flashbay.info())

#date_posted: split into two columns, one for hour of day, one for date, then convert date to datetime format
#create new column indicating the amount of time that has passed between date_posted and date_of_experience


print("Missing values:")
print(df_flashbay.isnull().sum())


#Up to here
print("This is the distribution of the types of variables in the dataset: ", "\n", df_flashbay.dtypes.value_counts())


print("These are the statistical distributions of the numeric variables present in the dataset: ", "\n")
print(df_flashbay.describe())

list = ['number_reviews', 'location', 'rating', 'verification']

for value in list:
    print(f"{value} has the following values", df_flashbay[value].value_counts())





print("Sample of data:")
print(df_flashbay.sample(5))

for column in df_flashbay.columns:
    print(f"\nUnique values in {column}:")
    print(df_flashbay[column].value_counts(dropna=False).head())

#Data that needs to be amended:
#text: apply text mining and sentiment analysis

#verification: convert to binary variable, then check relevance
#subject: apply text mining and sentiment analysis
#Missing values
#Duplicate entries


#df.replace(to_replace = x, value=y)
#df = df.rename({'old_name': 'new_name'}, axis = 1)
#df_lines = df.apply(np.sum, axis = 0)

#Calculate MSE
#create one dats
#df = df.loc[df['col 2'] == 3]
#df.merge(right=df2, on=x, how=z) or pd.concat([df1, df2], axis)
#df.groupby('column_name')
#caracteres_speciaux = [',', ':', ';', '.']
#def possib (word):
#    Liste = []
#    Liste.append(' ' + word + ' ')
#    for carac in caracteres_speciaux :      
#        Liste.append(' ' + word + carac)
#    Liste.append(word.capitalize() + ' ')
#    for carac in caracteres_speciaux :
#        Liste.append(word.capitalize() + carac)
#    return Liste
#print(possib(word = 'word'))

#from dico import *
#df['product_variation_size_id'] = df['product_variation_size_id'].map(dico_size)