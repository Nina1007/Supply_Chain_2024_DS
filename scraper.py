#This file is used to scrape the data for the company Flashbay from Trustpilot.
#The data is then stored in a csv file called 'data_flashbay.csv', unaltered.

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
            # Extract data with more robust error handling
            username = extract_text(card, 'span', class_='typography_heading-xxs__QKBS8')
            number_review = extract_text(card, 'span', attrs={'data-consumer-reviews-count-typography': 'true'})
            location = extract_text(card, 'div', attrs={'data-consumer-country-typography': 'true'})
            rating = extract_rating(card)
            text = extract_text(card, 'p', class_='typography_body-l__KUYFJ')
            date_of_experience = extract_date_of_experience(card)
            date_posted = extract_date_posted(card)
            verification = extract_text(card, 'div', class_='styles_reviewLabel__IPaZd')
            subject = extract_text(card, 'h2', class_='typography_heading-s__f7029')
            
            # Validate data types
            if not validate_data_types(username, number_review, location, rating, text, date_of_experience, date_posted, verification, subject):
                raise ValueError("Data validation failed")

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
                'page_number': page_number
            })
        except Exception as e:
            print(f"Error processing a review on page {page_number}: {e}")
    
    return page_data

def extract_text(element, tag, **attrs):
    found = element.find(tag, attrs)
    return found.text.strip() if found else ''

def extract_rating(card):
    rating_element = card.find('img', alt=lambda x: x and 'Rated' in x)
    if rating_element:
        alt_text = rating_element.get('alt', '')
        rating = alt_text.split('Rated')[1].split('out')[0].strip()
        return int(rating) if rating.isdigit() else None
    return None

def extract_date_of_experience(card):
    element = card.find('p', class_='typography_body-m__xgxZ_ typography_appearance-default__AAY17', attrs={'data-service-review-date-of-experience-typography': 'true'})
    if element:
        date_text = element.text.strip()
        return date_text.split('Date of experience:', 1)[-1].strip()
    return ''

def extract_date_posted(card):
    element = card.find('time')
    if element:
        timestamp = element.get('datetime')
        if timestamp:
            date_obj = datetime.fromisoformat(timestamp.rstrip('Z'))
            return date_obj.strftime('%Y-%m-%d %H:%M:%S')
    return ''

def validate_data_types(username, number_review, location, rating, text, date_of_experience, date_posted, verification, subject):
    if not isinstance(username, str) or not isinstance(number_review, str) or not isinstance(location, str):
        return False
    if rating is not None and not isinstance(rating, int):
        return False
    if not isinstance(text, str) or not isinstance(date_of_experience, str) or not isinstance(date_posted, str):
        return False
    if not isinstance(verification, str) or not isinstance(subject, str):
        return False
    return True

# Loop through all pages
def main():
    all_reviews = []
    max_retries = 3
    retry_delay = 5

    for page in range(1, 2):
        url = f'https://www.trustpilot.com/review/www.flashbay.com?page={page}'
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
    df_flashbay = pd.DataFrame(all_reviews)

#Save csv in Github repo
    github_repo_path = os.path.dirname(os.path.abspath(__file__))
    csv_filename = os.path.join(github_repo_path, 'data_flashbay_test.csv')

# Save the DataFrame to a CSV file
    df_flashbay.to_csv(csv_filename, index=False)
    print(f"Data saved to {csv_filename}")

# Output evaluation
    print("Total number of reviews:", len(df_flashbay))
    print("Number of duplicate entries: ", df_flashbay.duplicated().sum())

if __name__ == "__main__":
    main()