# Supply_Chain_2024_DS

# scraper_flashbay.py exports data from the Trustpilot website for company Flashbay and saves the data to a dataset called data_flashbay.csv
# scraper_flashbay_cleaning.py inspects the data_flashbay.csv dataset and removes rows that did not have the correct data extracted. This is because the structure of the Trustpilot website changes for older posts. The cleaned dataset is then stored in data_flashbay_clean.csv

# scraper_steelseries.py exports data from the Trustpilot website for company SteelSeries and saves the data to a dataset called data_steelseries.csv
# scraper_steelseries_cleaning.py inspects the data_steelseries.csv dataset and removes rows that did not have the correct data extracted. This is because the structure of the Trustpilot website changes for older posts. The cleaned dataset is then stored in data_steelseries_clean.csv

# scraper_asda.py exports data from the Trustpilot website for company Asda and saves the data to a dataset called data_asda.csv
# scraper_asda_cleaning.py inspects the data_asda.csv dataset and removes rows that did not have the correct data extracted. This is because the structure of the Trustpilot website changes for older posts. The cleaned dataset is then stored in data_asda_clean.csv

# scraper_quicken.py exports data from the Trustpilot website for company Quicken and saves the data to a dataset called data_quicken.csv
# scraper_quicken_cleaning.py inspects the data_quicken.csv dataset and removes rows that did not have the correct data extracted. This is because the structure of the Trustpilot website changes for older posts. The cleaned dataset is then stored in data_quicken_clean.csv


# initial_data_cleaning_trustpilot.ipynb - accomplishes the following:
# 1.	Merge datasets
# 2.	Remove obviously non-critical columns
# 3.	Convert dtypes appropriately
# 4.	Remove duplicates
# 5.	Handle N/A values
# 6.	Fix content standardization (e.g., 'customer' vs 'Customer')
# 7.	Show distribution of target variable
# 8.	Target variable .describe(), mean, mode, median
# 9.	Show class balance/imbalance
# produces data_trustpilot_first.csv

# initial_feature_processing.ipynb - accomplishes the following:
# 1.    Filtering out non-EN text rows
# 2.	Create additional useful columns from existing data
# 3.    Basic text preprocessing such as:
#       - initial cleaning, 
#       - removing of stop words, punctuations, and special characters, 
#       - calculating text length, 
#       - tokenizing and counting word frequencies, 
#       - most common words, 
#       - basic sentiment scores, 
#       - identifying words and phrases that might indicate positive or negative reviews
# produces data_trustpilot.csv

# exploratory_data_analysis_trustpilot.ipynb - accomplishes the following:
# 1.	Univariate analysis using .describe, mean, mode, median, data visualizations, Q-Q plot, word-frequency plots
# 2.	Multivariate analysis with target data visualizations, mean ratings by category, groupbys for numeric variables, word length distribution by rating
# 3.    Wordclouds
# 4.	Time series plot 
# 5.	Perform groupby analyses for location, company and username
# produces data_trustpilot_2.csv

# advanced_feature_processing.ipynb - accomplishes the following:
# 1.	Train/test split with stratification for ratings
# 2.	Handle outliers on training data only
# 3.    TF-IDF with n-grams
# 4.    Bag-of-words
# produces data_trustpilot_3.csv, train_trustpilot_3.csv, test_trustpilot_3.csv, X_train_tfidf.npy, X_test_tfidf.npy, tfidf_features.npy, X_train_bow.npy', X_test_bow.npy, bow_features.npy

# feature_selection.ipynb - accomplishes the following:
# 1.	Heat map of numeric variables correlations
# 2.	Checking for multicollinearity
# 3.	Pearson and Spearman 
# 4.	Mutual Information
# 5.	ANOVA test
# 6.	Variance threshold
# 7.	Fisher score
# 8.	Mean Absolute Difference
# 9.	Dispersion ratio
# 10.	Kruskal-Wallis test
# 11.	Recursive Feature Elimination
# 12.	LASSO
# 13.	Random Forest importance
# 14.	Logistic regression analysis for variable relationships including rig ratio
# 15.	Validate and compare methods
# 16.	Scaling/nornalization/standardization
# 17.   Dimensionality reduction if needed
# 18.   Oversampling/undersampling
# 19.   Cross-validation    
# 20.	Update train/test split for training and test data based on feature selection
# produces data_trustpilot_4.csv, train_final.csv, test_final.csv, final_features.txt   
