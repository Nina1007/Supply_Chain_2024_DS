# Supply_Chain_2024_DS

# 1.scraper_trustpilot.py exports data from the Trustpilot website for for numerous companies, adds the company name as a column and removes rows that did not have the correct data extracted due to structural changes to the website over time. Saves the data to a dataset called data_trustpilot_clean.csv

# 2.initial_data_cleaning_trustpilot.ipynb - accomplishes the following:
# 1.	Remove obviously non-critical columns
# 2.	Convert dtypes appropriately
# 3.	Remove duplicates
# 4.	Handle N/A values
# 5.	Fix content standardization (e.g., 'customer' vs 'Customer')
# 6.	Show distribution of target variable
# 7.	Target variable .describe(), mean, mode, median
# 8.	Show class balance/imbalance
# produces data_trustpilot_first.csv

# 3.initial_feature_processing.ipynb - accomplishes the following:
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

# 4.exploratory_data_analysis_trustpilot.ipynb - accomplishes the following:
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
# 2.	Encoding
# 3.	Scaling/nornalization/standardization
# 4.	Variance threshold
# 5.    Mean Absolute Difference
# 6.	Pearson and Spearman 
# 7.	ANOVA test
# 8.	Mutual Information
# 9.	Kruskal-Wallis test
# 10.	Recursive Feature Elimination
# 11.	LASSO
# 12.	Random Forest importance
# 13.	Logistic regression analysis for variable relationships including rig ratio
# 14.	Checking for multicollinearity
# 15.	Feature selection with cross-validation
# 16.	Update train/test split for training and test data based on feature selection
# produces X_train.csv, X_test.csv, y_train.csv, y_test.csv  
