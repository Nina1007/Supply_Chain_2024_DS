import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import time
import pandas as pd
import numpy as np
import re
import os

def scrape_trustpilot(companies_config):
    def scrape_page(url, page_number): 
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers)
        soup = bs(response.content, 'lxml')
        review_cards = soup.find_all('article', class_='paper_paper__1PY90')
        page_data = []
        for card in review_cards:
            try:
                text_element = card.find('p', class_='typography_body-l__KUYFJ')
                if not text_element:
                    continue  
                
                data = {
                'username': card.find('span', class_='typography_heading-xxs__QKBS8').text.strip(),
                'number_reviews': card.find('span', attrs={'data-consumer-reviews-count-typography': 'true'}).text.strip(),
                'location': card.find('div', attrs={'data-consumer-country-typography': 'true'}).text.strip(),
                'rating': card.find('img', alt=lambda x: x and 'Rated' in x).get('alt').split('Rated')[1].split('out')[0].strip(),
                'text': text_element.get_text(separator=' ').strip(),
                'date_posted': datetime.fromisoformat(card.find('time')['datetime'].rstrip('Z')).strftime('%Y-%m-%d %H:%M:%S'),
                'date_of_experience': card.find('p', attrs={'data-service-review-date-of-experience-typography': 'true'}).text.split('Date of experience:', 1)[-1].strip(),
                'verification': card.find('div', class_='styles_reviewLabel__IPaZd').text.strip() if card.find('div', class_='styles_reviewLabel__IPaZd') else '',
                'subject': card.find('h2', class_='typography_heading-s__f7029').text.strip() if card.find('h2', class_='typography_heading-s__f7029') else '',
                'answer': card.find('p', attrs={'data-service-review-business-reply-text-typography': 'true'}).text.strip() if card.find('p', attrs={'data-service-review-business-reply-text-typography': 'true'}) else '',
                'page_number': page_number}
                page_data.append(data)
            except Exception as e:
                print(f"Error processing review on page {page_number}: {e}")
        return page_data

    def clean_dataframe(df, company_name):
        def is_valid(value, expected_type):
            if pd.isna(value): return False
            if expected_type == 'rating':
                try: return float(str(value).strip()) in [1.0, 2.0, 3.0, 4.0, 5.0]
                except ValueError: return False
            elif expected_type in ['date_posted', 'date_of_experience']:
                if not isinstance(value, str): return False
                formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%B %d, %Y', '%d/%m/%Y']
                return any(True for fmt in formats if try_parse_date(value, fmt))
            elif expected_type == 'location':
                return isinstance(value, str) and len(value.strip()) > 0
            elif expected_type == 'number_reviews':
                return bool(re.findall(r'\d+', str(value)))
            return True

        def try_parse_date(value, fmt):
            try:
                datetime.strptime(value, fmt)
                return True
            except ValueError:
                return False

        df['company'] = company_name
        df['issues'] = df.apply(lambda row: [col for col in ['rating', 'date_posted', 'date_of_experience', 'location', 'number_reviews'] 
                                           if not is_valid(row[col], col)], axis=1)
        clean_df = df[df['issues'].apply(len) == 0].drop('issues', axis=1)
        print(f"{company_name} - Original rows: {len(df)}, Clean rows: {len(clean_df)}")
        return clean_df

    all_companies_data = []
    for company in companies_config:
        company_reviews = []
        for page in range(1, company['pages'] + 1):
            url = f'https://www.trustpilot.com/review/{company["url"]}?page={page}'
            print(f"Scraping {company['name']} - page {page}")
            for attempt in range(3):
                try:
                    page_data = scrape_page(url, page)
                    company_reviews.extend(page_data)
                    time.sleep(2)
                    break
                except Exception as e:
                    print(f"Error on page {page}, attempt {attempt + 1}: {e}")
                    time.sleep(5)

        if company_reviews:
            df = pd.DataFrame(company_reviews)
            clean_df = clean_dataframe(df, company['name'])
            all_companies_data.append(clean_df)

    if all_companies_data:
        df_trustpilot = pd.concat(all_companies_data, ignore_index=True)
        print("Final dataset columns:", df_trustpilot.columns.tolist())
        print("Rows per company:", df_trustpilot['company'].value_counts())
        df_trustpilot.to_csv('data/data_trustpilot_clean.csv', index=False)
        return df_trustpilot
    return None

companies = [{'name': 'Asda', 'url': 'www.asda.com', 'pages': 807},
     {'name': 'SteelSeries', 'url': 'www.steelseries.com', 'pages': 888},
     {'name': 'Quicken', 'url': 'www.quicken.com', 'pages': 1712},
     {'name': 'Rebtel', 'url': 'www.rebtel.com', 'pages': 343},
     {'name': 'SmarterPhone', 'url': 'smarter-phone.co', 'pages': 32},
     {'name': 'LegalMatch', 'url': 'legalmatch.com', 'pages': 133},
     {'name': 'Solis', 'url': 'skyroam.com', 'pages': 111},
     {'name': 'CheckURL', 'url': 'international-iq-test.com', 'pages': 90},
     {'name': 'BeenVerified', 'url': 'www.beenverified.com', 'pages': 108},
     {'name': 'FreedomPop', 'url': 'freedompop.com', 'pages': 82},
     {'name': 'DSLExtreme', 'url': 'dslextreme.com', 'pages': 58},
     {'name': 'HubbleConnected', 'url': 'hubbleconnected.com', 'pages': 48},
     {'name': 'ConnectWise', 'url': 'connectwise.com', 'pages': 41},
     {'name': 'HubSpot', 'url': 'hubspot.com', 'pages': 34},
     {'name': 'SpyTecGPS', 'url': 'www.spytec.com', 'pages': 39},
     {'name': 'Pigeonly', 'url': 'pigeonly.com', 'pages': 33},
     {'name': 'Kandco', 'url': 'www.kandco.com', 'pages': 36},
     {'name': 'SCUFGaming', 'url': 'scufgaming.com', 'pages': 704},
     {'name': 'Inkfarm.com', 'url': 'www.inkfarm.com', 'pages': 1549},
     {'name': 'StockX', 'url': 'stockx.com', 'pages': 6357},
     {'name': 'CASETiFY', 'url': 'casetify.com', 'pages': 4280},
     {'name': 'Toluna', 'url': 'www.toluna.com', 'pages': 1851},
     {'name': 'PDFSimpli', 'url': 'pdfsimpli.com', 'pages': 3555},
     {'name': 'SurveyJunkie', 'url': 'www.surveyjunkie.com', 'pages': 2108}]
df = scrape_trustpilot(companies)