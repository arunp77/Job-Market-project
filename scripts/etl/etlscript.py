import pandas as pd
from deep_translator import GoogleTranslator
import os
from datetime import datetime

# Translation dictionary
translation_dict = {
    "Werkstudent": "working student",
    "Praktikum": "internship",
    "Teamassistenz": "team assistant",
    "Werkstudent*in": "working student",
}

def translate_to_english(text):
    translation = GoogleTranslator(source='auto', target='en').translate(text)
     # Replace words using the translation dictionary
    for key, value in translation_dict.items():
        translation = translation.replace(key, value)

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

def translate_csv(input_csv, output_csv,columns_to_translate=None, timestamp_conversion=None, date_column=None):
    # Read the CSV file
    df = pd.read_csv(input_csv)

   
    # Translate specified columns
    if columns_to_translate is not None:
        for column in columns_to_translate:
            if column in df.columns:
                try:
                    df.loc[:, column] = df[column].apply(translate_to_english)
                except OSError as e:
                    print(f"Error translating column '{column}': {e}")

    # Changing the timestamp : removing time from the datetimestamp
    if date_column and timestamp_conversion:
        df.loc[:, date_column] = df[date_column].apply(timestamp_conversion)
    # Create output folder if it doesn't exist
    os.makedirs(output_csv, exist_ok=True)
    
    # Save the translated DataFrame to a new CSV file
    output_file_path = os.path.join(output_csv, os.path.basename(input_csv))
    df.to_csv(output_file_path, index=False)

    print(f"Data processed successfully for the file {os.path.basename(input_csv)}")


def main():
     # Paths to input CSV files
    adzuna_input_path = '../../data/scraped_data/adjurna/csv/adzuna_scrapped_data.csv'
    muse_input_path = '../../data/scraped_data/muse/csv/muse_scrapped_data.csv'
    stepstone_input_path = '../../data/scraped_data/ss/ss_datascience_germany_20240221.csv'
    
    # Paths to output folders
    adzuna_output_path = '../../data/processed_data/adjurna_processed_data'
    muse_output_path = '../../data/processed_data/muse_processed_data'
    stepstone_output_path = '../../data/processed_data/ss_processed_data'

    columns_to_translate_adzuna = ['title', 'category','source','description']
    columns_to_translate_muse = ['Job Title']
    columns_to_translate_stepstone = ['title']

    date_variable_for_adzuna = 'job_posted'
    date_variable_for_muse = 'Publication Date'

    # Clean and save data
    translate_csv(adzuna_input_path, adzuna_output_path,columns_to_translate_adzuna,remove_time_from_timestamp_for_adzuna,date_variable_for_adzuna)
    translate_csv(muse_input_path, muse_output_path,columns_to_translate_muse,remove_time_from_timestamp_for_muse,date_variable_for_muse)
    translate_csv(stepstone_input_path, stepstone_output_path,columns_to_translate_stepstone)


if __name__ == "__main__":
    main() 

