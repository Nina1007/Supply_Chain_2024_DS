#This file is used to scrape the data for the company SteelSeries from Trustpilot.
#The data is then stored in a csv file called 'data_steelseries.csv', unaltered.

import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import time
import pandas as pd
import os

def scrape_page(url, page_number):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    content = response.content
    soup = bs(content, 'lxml')
    review_cards = soup.find_all('article', class_='paper_paper__1PY90')
    
    page_data = []
    
    for card in review_cards:
        try:
            username_element = card.find('span', class_='typography_heading-xxs__QKBS8')
            number_review_element = card.find('span', attrs={'data-consumer-reviews-count-typography': 'true'})
            location_element = card.find('div', attrs={'data-consumer-country-typography': 'true'})
            rating_element = card.find('img', alt=lambda x: x and 'Rated' in x)
            text_element = card.find('p', class_='typography_body-l__KUYFJ')
            date_of_experience_element = card.find('p', class_='typography_body-m__xgxZ_ typography_appearance-default__AAY17', attrs={'data-service-review-date-of-experience-typography': 'true'})            
            verification_element = card.find('div', class_='styles_reviewLabel__IPaZd')
            date_posted_element = card.find('time')
            subject_ranking_element = card.find('h2', class_='typography_heading-s__f7029')
            answer_element = card.find('p', attrs={'data-service-review-business-reply-text-typography': 'true'})
            
            username = username_element.text.strip() if username_element else ''
            number_review = number_review_element.text.strip() if number_review_element else ''
            location = location_element.text.strip() if location_element else ''
            text = text_element.text.strip() if text_element else ''
            verification = verification_element.text.strip() if verification_element else ''
            subject = subject_ranking_element.text.strip() if subject_ranking_element else ''
            answer = answer_element.text.strip() if answer_element else ''

            date_of_experience = ''
            if date_of_experience_element:
                date_text = date_of_experience_element.text.strip()
                date_of_experience = date_text.split('Date of experience:', 1)[-1].strip()

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
                'subject': subject,
                'page_number': page_number,
                'answer': answer
            })
        except Exception as e:
            print(f"Error processing a review on page {page_number}: {e}")
    
    return page_data

# Loop through all pages
def main():
    all_reviews = []
    max_retries = 3
    retry_delay = 5

    for page in range(1, 889):
        url = f'https://www.trustpilot.com/review/www.steelseries.com?page={page}'
        print(f"Scraping page {page}...")
        
        for attempt in range(max_retries):
            try:
                page_data = scrape_page(url, page)
                all_reviews.extend(page_data)
                print(f"Added {len(page_data)} reviews from page {page}")
                time.sleep(2) 
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Error scraping page {page}: {e}. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"Failed to scrape page {page} after {max_retries} attempts: {e}")


# Create a DataFrame from the collected data
    df_steelseries = pd.DataFrame(all_reviews)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

#Save csv in Github repo
    github_repo_path = os.path.dirname(os.path.abspath(__file__))
    csv_filename = 'data_steelseries.csv'
    full_path = os.path.join(data_dir, csv_filename)

# Save the DataFrame to a CSV file
    df_steelseries.to_csv(full_path, index=False)
    print(f"Data saved to {csv_filename}")

# Output evaluation
    print("Total number of reviews:", len(df_steelseries))
    print("Number of duplicate entries: ", df_steelseries.duplicated().sum())

if __name__ == "__main__":
    main()

