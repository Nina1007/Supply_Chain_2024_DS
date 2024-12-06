# gpt_enhancement.py
import sys
import openai
import pandas as pd
import numpy as np
import time
from tqdm import tqdm
import json
import logging
from concurrent.futures import ThreadPoolExecutor
import asyncio
import aiohttp
from config import OPENAI_API_KEY

def process_review(client, text, delay=1):
    try:
        time.sleep(delay)
        response = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful review analyzer."}, {"role": "user", "content": f"Analyze this review: {text}"}], temperature=0.3, max_tokens=100)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error processing review: {str(e)}")
        return None

def process_batch(client, batch_texts, delay=1):
    results = []
    with ThreadPoolExecutor(max_workers=len(batch_texts)) as executor:
        futures = [executor.submit(process_review, client, text, delay)
            for text in batch_texts]
        results = [f.result() for f in futures]
    return results

def enhance_dataset(input_file, output_file, sample_size=None, batch_size=5):
    try:
        print("Loading data...")
        df = pd.read_csv(input_file)
        if sample_size:
            df = df.sample(n=min(sample_size, len(df)), random_state=42)
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        print(f"Processing {len(df)} reviews in batches of {batch_size}...")
        gpt_responses = []
        for i in tqdm(range(0, len(df), batch_size)):
            batch = df.iloc[i:i+batch_size]
            batch_texts = batch['text'].tolist()
            batch_responses = process_batch(client, batch_texts)
            gpt_responses.extend(batch_responses)
            time.sleep(2)
        features_df = df.drop(['rating'], axis=1)
        features_df['gpt_analysis'] = gpt_responses
        base_name = output_file.replace('.csv', '')
        features_df.to_csv(f'{base_name}_X.csv', index=False)
        df[['rating']].to_csv(f'{base_name}_y.csv', index=False)
        print(f"Saved enhanced dataset to {base_name}_X.csv and {base_name}_y.csv")
        return features_df, df[['rating']]
    except Exception as e:
        print(f"Error in enhancement process: {str(e)}")
        raise

if __name__ == "__main__":
    input_file = 'data/train_trustpilot_3.csv'
    output_file = 'data/enhanced_train_sample.csv'
    features_df, ratings_df = enhance_dataset(input_file, output_file,  sample_size=3, batch_size=5)
    print("Sample of enhanced data:")
    print(features_df[['text', 'gpt_analysis']].head())