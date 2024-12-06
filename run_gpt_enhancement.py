from gpt_enhancement import enhance_dataset
import time

if __name__ == "__main__":
    sample_size = 1000
    
    print(f"Processing {sample_size} training reviews...")
    train_enhanced, train_ratings = enhance_dataset( 
        input_file='data/train_trustpilot_3.csv',
        output_file='data/train_trustpilot_3_enhanced_100.csv',
        sample_size=sample_size)
        
    time.sleep(10)
    
    print(f"Processing {sample_size} test reviews...")
    test_enhanced, test_ratings = enhance_dataset( 
        input_file='data/test_trustpilot_3.csv',
        output_file='data/test_trustpilot_3_enhanced_100.csv',
        sample_size=sample_size)
        
    print("Summary of enhanced data:")
    print(f"Training samples processed: {len(train_enhanced)}")
    print(f"Test samples processed: {len(test_enhanced)}")
    
    print("Sample analyses across different ratings:")
    for rating in train_ratings['rating'].unique():
        sample_idx = train_ratings[train_ratings['rating'] == rating].index[0]
        sample = train_enhanced.iloc[sample_idx]
        print(f"\nRating {rating}:")
        print(f"Text: {sample['text'][:100]}...")
        print(f"Analysis: {sample['gpt_analysis'][:100]}...")