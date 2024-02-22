import pandas as pd
import os

def clean_data_and_save(input_path, output_path):
    # Read CSV file
    df = pd.read_csv(input_path)
    
    # Clean the data (You can add your data cleaning steps here)
    cleaned_df = df.dropna()  
    
    # Create output folder if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Save processed data to CSV
    output_file_path = os.path.join(output_path, os.path.basename(input_path))
    cleaned_df.to_csv(output_file_path, index=False)
    print(f"Processed data saved to {output_file_path}")

def main():
    # Paths to input CSV files
    ajurna_input_path = '../../data/scraped_data/ajurna/csv/adzuna_scrapped_data.csv'
    muse_input_path = '../../data/scraped_data/muse/csv/muse_scrapped_data.csv'
    
    # Paths to output folders
    ajurna_output_path = '../../data/processed_data/adjurna_processed_data'
    muse_output_path = '../../data/processed_data/muse_processed_data'
    
    # Clean and save data
    clean_data_and_save(ajurna_input_path, ajurna_output_path)
    clean_data_and_save(muse_input_path, muse_output_path)

if __name__ == "__main__":
    main() 
