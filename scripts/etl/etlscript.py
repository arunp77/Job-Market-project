import pandas as pd
from deep_translator import GoogleTranslator
import os
from datetime import datetime

def translate_to_english(text):
    translation = GoogleTranslator(source='auto', target='en').translate(text)
    return translation


def remove_time_from_timestamp_for_muse(timestamp):
    # Convert the timestamp to a datetime object
    datetime_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    # Format the datetime object without the time part
    date_without_time = datetime_obj.strftime("%Y-%m-%d")

    return date_without_time

def remove_time_from_timestamp_for_adzuna(timestamp):
    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    formatted_date = timestamp.strftime('%Y-%m-%d')
    return formatted_date

def translate_csv(input_csv, output_csv,columns_to_translate, timestamp_conversion, date_column):
    # Read the CSV file
    df = pd.read_csv(input_csv)

    #dropping the null fields in the file 
    df_null_dropped = df.dropna()  

   
    # Translate specified columns
    for column in columns_to_translate:
        print("column", column)
        if column in df_null_dropped.columns:
            try:
                for row in df_null_dropped[column]:
                    translated_column = translate_to_english(row)
                    row = translated_column
            except OSError as e:
                print(f"Error translating column '{column}': {e}")

    # Changing the timestamp : removing time from the datetimestamp
    df_null_dropped[date_column] = df_null_dropped[date_column].apply(timestamp_conversion)

    # Create output folder if it doesn't exist
    os.makedirs(output_csv, exist_ok=True)
    
    # Save the translated DataFrame to a new CSV file
    output_file_path = os.path.join(output_csv, os.path.basename(input_csv))
    df_null_dropped.to_csv(output_file_path, index=False)


def main():
     # Paths to input CSV files
    ajurna_input_path = 'adzuna_scrapped_data.csv'
    muse_input_path = '../../data/scraped_data/muse/csv/muse_scrapped_data.csv'
    
    # Paths to output folders
    ajurna_output_path = 'adjurna_processed_data'
    muse_output_path = '../../data/processed_data/muse_processed_data'

    columns_to_translate = ['title', 'category','source','description']
    columns_to_translate_muse = ['Job Title']

    # Clean and save data
    translate_csv(ajurna_input_path, ajurna_output_path,columns_to_translate,remove_time_from_timestamp_for_adzuna,'job_posted')
    translate_csv(muse_input_path, muse_output_path,columns_to_translate_muse,remove_time_from_timestamp_for_muse,'Publication Date')


if __name__ == "__main__":
    main() 

