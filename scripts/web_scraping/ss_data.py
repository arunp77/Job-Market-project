#!/usr/bin/env python3
# SS fetch data
# Name : BS,  version: 1  Date : 20240219
from bs4 import BeautifulSoup as bs
import urllib.request
import pandas as pd
from datetime import datetime, timedelta
import os
from deep_translator import GoogleTranslator
import logging
import json

def convert_relative_time_to_date(num,relative_time):
    current_datetime = datetime.now()
    num = int(num)
    if 'hours' in relative_time or 'hour' in relative_time:
        converted_date = current_datetime - timedelta(hours=num)
    elif 'days' in relative_time or 'day' in relative_time:
        converted_date = current_datetime - timedelta(days=num)
    elif 'weeks' in relative_time or 'week' in relative_time:
        converted_date = current_datetime - timedelta(weeks=num)
    elif 'months' in relative_time or 'month' in relative_time:
        converted_date = current_datetime - timedelta(months=num)
    else:
        converted_date = ""

    return converted_date.strftime('%Y-%m-%d')

def translate_german_to_english(text):
    translator = GoogleTranslator()
    translated = translator.translate(text, source='de', target='en')
    return translated

def compute_job_details(source_file):
    res = open(source_file, "r", encoding="utf8")
    soup_meta = bs(res, 'html.parser')
    job_details = soup_meta.find_all("article", class_="res-1p8f8en")
   # job_details = soup_meta.find_all("article", class_=lambda c: c and c.startswith("res-1"))


    #print(job_details)
    titles, companys, locations, day_before_posts, day_before_posts_en, date_posts, ref_links = [], [], [], [], [], [], []
    for job_detail in job_details:
        company = job_detail.find("div", class_="res-1r68twq").text.strip()
        companys.append(company)
        title = job_detail.find("div", class_="res-nehv70").text.strip()
        titles.append(title)
        location = job_detail.find("div", class_="res-qchjmw").text.strip()
        locations.append(location)
        day_before_post = job_detail.find("div", class_="res-7skf5p").text.strip()
        day_before_posts.append(day_before_post)
        date_post = translate_german_to_english(day_before_post)
        day_before_posts_en.append(date_post)
        date_post = convert_relative_time_to_date(date_post.split(" ")[0], date_post)
        date_posts.append(date_post)
        ref_link = job_detail.find("a", class_="res-5rh28j")['href']
        ref_links.append("https://www.stepstone.de" + ref_link)
    list_ = list(zip(titles, companys, locations, day_before_posts, day_before_posts_en, date_posts, ref_links))

    df = pd.DataFrame(list_,
                          columns=["title", "company", "location", "day_before_posts_de", "day_before_posts_en",
                                   "job_posted", "link"])

    return df


def handler():

    try:

        # Get the current script's directory
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Create the path to the file in the 'src_data' folder
        src_path = os.path.join(script_dir, 'htmlfiles')

        df_final = pd.DataFrame()
        # List all files in the directory
        files = [f for f in os.listdir(src_path) if f.lower().endswith('.html')]

        # Iterate over each CSV file and read into the DataFrame
        for file_name in files:
            src_file_path = os.path.join(src_path, file_name)
            # Read CSV file into corresponding DataFrame
            df = compute_job_details(src_file_path)
            df_final = pd.concat([df_final, df], ignore_index=True)
        write_file_path = script_dir.replace("\scripts\web_scraping", "\data\scraped_data\ss")
        print(write_file_path)
        final_file_path_csv = os.path.join(write_file_path, "ss.csv")
        final_file_path_json = os.path.join(write_file_path, "ss.json")
        print(len(df_final))

        df_final.to_csv(final_file_path_csv, index=False, header=True)
        # Write list of dictionaries to JSON file
        records = df_final.to_dict(orient='records')
        with open(final_file_path_json, 'w', encoding='utf-8') as json_file:
            for record in records:
                json.dump(record, json_file, ensure_ascii=False)
                json_file.write('\n')
        print(final_file_path_json)
    except Exception as e:
        logging.error(f"An unexpected error occurred in the main block: {e}")
        raise

if __name__ == "__main__":

    handler()