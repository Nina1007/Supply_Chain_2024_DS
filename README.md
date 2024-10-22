# Supply_Chain_2024_DS

# scraper_flashbay.py exports data from the Trustpilot website for company Flashbay and saves the data to a dataset called data_flashbay.csv
# scraper_flashbay_cleaning.py inspects the data_flashbay.csv dataset and removes rows that did not have the correct data extracted. This is because the structure of the Trustpilot website changes for older posts. The cleaned dataset is then stored in data_flashbay_clean.csv

# scraper_steelseries.py exports data from the Trustpilot website for company SteelSeries and saves the data to a dataset called data_steelseries.csv
# scraper_steelseries_cleaning.py inspects the data_steelseries.csv dataset and removes rows that did not have the correct data extracted. This is because the structure of the Trustpilot website changes for older posts. The cleaned dataset is then stored in data_steelseries_clean.csv

# scraper_asda.py exports data from the Trustpilot website for company Asda and saves the data to a dataset called data_asda.csv
# scraper_asda_cleaning.py inspects the data_asda.csv dataset and removes rows that did not have the correct data extracted. This is because the structure of the Trustpilot website changes for older posts. The cleaned dataset is then stored in data_asda_clean.csv


# preprocessor_trustpilot.py reads datasets data_flashbay_clean.csv, data_steelseries_clean.csv and data_asda.csv and, upon verifying that the columns and shapes of the three datasets match, concatenates them into df_trustpilot. The corresponding columns are:
# 'username': Name of the user who submitted the review
# 'number_reviews': Number of reviews the user has submitted on the Trustpilot platform to date
# 'location': the two-digit countrycode of the user
# 'rating': rating as submitted by the user on a scale from 1 (very bad) to 5 (very good)
# 'text': the text description the user submitted as part of their review
# 'date_of_experience': the date on which the user experienced (most likely purchased) the product
# 'date_posted': date and time of the post 
# 'verification': indicates whether the user is a verified user or not 
# 'subject': subject line accompanying the text of the review
# 'page_number': page number of the website from which the data was scraped
# Including the index column, the initial dataframe df_trustpilot contains 10 columns and 36,017 rows

# preprocessor_trustpilot.py further investigates the data of the merged dataset from Trustpilot called df_trustpilot. The following changes to the data occur:
# 'number_reviews': Initial data in the cell included e.g. '1 review'. The 'review(s)' was deleted from all cells and the type was changed from object to integer.
# 'date_of_experience': Type was changed from object to datetime
# 'date_posted': Type was changed from object to datetime and then the data was split into two columns. The 'date_posted' columns was changed to include the date only, without the time
# 'hour_posted': newly created column, includes the time of the post in military time
# 'day_of_week_posted': newly created column, includes the day of the week in letter format (e.g. 'Monday') of when the post was created
# 'days_between_experience_and_post': newly created column, indicates the amount of time (in days) that has passed between the logged date_of_experience and the date_posted
# 'page_number': is deleted due to the irrelevance of the data



# data_trustpilot.csv includes the following checks on the data: all rows have correct entries in their columns, dtype correctness, splitting of data into relevant columns, removed duplicates, filled n/a values for 'customer' with the most frequently used username from the dataset which is 'Customer', filled n/a values for 'verification' with a new variable indicating that no verification has taken place with 'Not Verified', removed n/a values for missing text object
# The following columns and descriptions:
# 'username': Name of the user who submitted the review
# 'number_reviews': Number of reviews the user has submitted on the Trustpilot platform to date
# 'location': the two-digit countrycode of the user
# 'rating': rating as submitted by the user on a scale from 1 (very bad) to 5 (very good)
# 'text': the text description the user submitted as part of their review
# 'date_of_experience': the date on which the user experienced (most likely purchased) the product
# 'verification': indicates whether the user is a verified user or not 
# 'subject': subject line accompanying the text of the review
# 'date_posted': includes the date of the post
# 'hour_posted': includes the time of the post in military time
# 'day_of_week_posted': includes the day of the week in letter format (e.g. 'Monday') of when the post was created
# 'days_between_experience_and_post': indicates the amount of time (in days) that has passed between the logged date_of_experience and the date_posted
# 12 columns, 33,276 rows of data