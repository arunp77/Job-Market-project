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
from selenium.webdriver import Chrome
import requests
import time
import csv
logging.basicConfig(filename='logfile.log', level=logging.DEBUG)

field = "data-science"
location = "germany"


def get_jobs_page(url,filename):
    driver = Chrome()
    driver.get(url)
    time.sleep(30)  # Sleep for 30 seconds
   # page_source = driver.page_source
    html = driver.page_source
    soup = bs(html, 'html.parser')

    #writing the html page in the page_source.html
    with open(filename, 'w', encoding='utf-8') as html_file:
        html_file.write(html)
    return soup

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

def compute_job_details(soup):

    job_details = soup.find_all("article", class_="res-1p8f8en")

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

    print(len(df))
    return df


def file_create_append(filename,df_final,csv_df = True):

    records = df_final.to_dict(orient='records')

    append_write = 'a' if os.path.isfile(filename) else 'w'
    if csv_df:
        with open(filename, append_write, newline='', encoding='utf-8') as csv_file:
            fieldnames = records[0].keys() if records else []
            writer = csv.DictWriter(csv_file,fieldnames = fieldnames)
            # Write header if the file is being created
            if append_write == 'w':
                writer.writeheader()
            # Write records
            for record in records:
                writer.writerow(record)

    else:
        # Write list of dictionaries to JSON file
        with open(filename, append_write, encoding='utf-8') as json_file:
            for record in records:
                json.dump(record, json_file, ensure_ascii=False)
                json_file.write('\n')


def handler():

    try:

        # Get the current script's directory
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Create the path to the file in the 'src_data' folder
        src_path = os.path.join(script_dir, 'htmlfiles')

        # final file path for job information(data)
        write_file_path = script_dir.replace("\scripts\web_scraping", "\data\scraped_data\ss")
        logging.info(write_file_path)
        final_file_path_csv = os.path.join(write_file_path, "ss_datascience_germany_20240221.csv")
        final_file_path_json = os.path.join(write_file_path, "ss_datascience_germany_20240221.json")

        df_final = pd.DataFrame()
        # List all files in the directory
        for i in range(1,51):
            URL = f'https://www.stepstone.de/jobs/{field}/in-{location}?radius=100&page={i}'
            logging.info(URL)
            html_file_path = os.path.join(src_path, f"ss_20240221_{i}.html")
            soup = get_jobs_page(URL, html_file_path)

            df = compute_job_details(soup)
            file_create_append(final_file_path_csv, df)
            file_create_append(final_file_path_json, df, False)
            print(f"iteration {i}, {len(df)} loaded successfully in the path csv {final_file_path_csv} and json {final_file_path_json}")
            logging.info(f"iteration {i}, {len(df)} loaded successfully in the path csv {final_file_path_csv} and json {final_file_path_json}")


    except Exception as e:
        logging.error(f"An unexpected error occurred in the main block: {e}")
        raise

if __name__ == "__main__":

    handler()