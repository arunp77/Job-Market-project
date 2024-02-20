import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
import pandas as pd
import json


URL = 'https://www.stepstone.de/work/full-stack-engineer/in-berlin?radius=30'
def get_jobs_page(url):
    driver = Chrome()
    driver.get(url)
    page_source = driver.page_source
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #writing the html page in the page_source.html

    with open('page_source.html', 'w', encoding='utf-8') as html_file:
        html_file.write(page_source)

    job_details = soup.find_all("article", class_="res-1p8f8en")
   
    titles, companies, locations = [],[],[]
    for job_detail in job_details:
        company = job_detail.find("div", class_="res-1r68twq").text.strip()
        companies.append(company)
        title = job_detail.find("div", class_="res-nehv70").text.strip()
        titles.append(title)
        location = job_detail.find("div", class_="res-qchjmw").text.strip()
        locations.append(location)
    list_ = list(zip(titles, companies, locations))

    df = pd.DataFrame(list_, columns=["title", "company", "location"])
    
    print(df)
    # Save the DataFrame to a JSON file
    df.to_json('jobs_data.json', orient='records', lines=True)

    # Save the DataFrame to a CSV file
    df.to_csv('jobs_data.csv', index=False)

    driver.quit()  # Don't forget to close the webdriver after use


 

get_jobs_page(URL)