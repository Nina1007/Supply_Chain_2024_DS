import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import time
import pandas as pd
import os

def scrape_page(url):
    response = requests.get(url)
    content = response.content
    soup = bs(content, 'lxml')
    review_cards = soup.find_all('article', class_='paper_paper__1PY90')
    
    page_data = []
    
    for card in review_cards:
        username_element = card.find('span', class_='typography_heading-xxs__QKBS8')
        number_review_element = card.find('span', class_='typography_body-m__xgxZ_')
        location_element = card.find('div', class_='typography_body-m__xgxZ_')
        rating_element = card.find('img', alt=lambda x: x and 'Rated' in x)
        text_element = card.find('p', class_='typography_body-l__KUYFJ')
        date_of_experience_element = card.find('p', class_='typography_body-m__xgxZ_')
        verification_element = card.find('div', class_='styles_reviewLabel__IPaZd')
        date_posted_element = card.find('time')
        subject_ranking_element = card.find('h2', class_='typography_heading-s__f7029')
        username = username_element.text.strip() if username_element else ''
        number_review = number_review_element.text.strip() if number_review_element else ''
        location = location_element.text.strip() if location_element else ''
        text = text_element.text.strip() if text_element else ''
        date_of_experience = date_of_experience_element.text.strip('Date of experience:') if date_of_experience_element else ''
        verification = verification_element.text.strip() if verification_element else ''
        subject = subject_ranking_element.text.strip() if subject_ranking_element else ''
        rating = ''
        if rating_element:
            alt_text = rating_element.get('alt', '')
            rating = alt_text.split('Rated')[1].split('out')[0].strip()
        date_posted = ''
        if date_posted_element:
            timestamp = date_posted_element.get('datetime')
            if timestamp:
                date_obj = datetime.fromisoformat(timestamp.rstrip('Z'))
                date_posted = date_obj.strftime('%Y-%m-%d %H:%M:%S')

        
        page_data.append({
            'username': username,
            'number_reviews': number_review,
            'location': location,
            'rating': rating,
            'text': text,
            'date_of_experience': date_of_experience,
            'date_posted': date_posted,
            'verification': verification,
            'subject': subject
        })
    
    return page_data

# Initialize an empty list to store all review data
all_reviews = []

# Loop through all pages
for page in range(1, 935):  # You might want to reduce this number for testing
    url = f'https://www.trustpilot.com/review/www.flashbay.com?page={page}'
    print(f"Scraping page {page}...")
    try:
        page_data = scrape_page(url)
        all_reviews.extend(page_data)
        time.sleep(1)
    except Exception as e:
        print(f"Error scraping page {page}: {e}")
        continue 

# Create a DataFrame from the collected data
df_trustpilot = pd.DataFrame(all_reviews)

#Save csv in Github repo
github_repo_path = os.path.dirname(os.path.abspath(__file__))
csv_directory = os.path.join(github_repo_path, 'data')
os.makedirs(csv_directory, exist_ok=True)
csv_filename = os.path.join(csv_directory, 'flashbay_trustpilot_reviews.csv')

# Save the DataFrame to a CSV file
csv_filename = 'flashbay_trustpilot_reviews.csv'
df_trustpilot.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")

# Output evaluation
print("Total number of reviews:", len(df_trustpilot))
print("Columns in the DataFrame:", df_trustpilot.columns.tolist())
print("First few rows of the DataFrame:")
print(df_trustpilot.head())