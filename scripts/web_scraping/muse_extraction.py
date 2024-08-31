import requests
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
import os

def load_api_key(env_var_name="API_KEY1"):
    """
    Load the API key from environment variables.

    :param env_var_name: Name of the environment variable.
    :return: API key as a string.
    """
    load_dotenv()
    return os.getenv(env_var_name)

def build_url(page_num):
    """
    Build the API request URL for a given page number.

    :param page_num: Page number to request.
    :return: A formatted URL string.
    """
    url_template = ('https://www.themuse.com/api/public/jobs?category=Computer%20and%20IT&'
                    'category=Data%20and%20Analytics&category=Data%20Science&category=IT&'
                    'level=Entry%20Level&level=Mid%20Level&level=Senior%20Level&level=management&'
                    'location=Berlin%2C%20DE&location=Berlin%2C%20Germany&location=Cologne%2C%20Germany&'
                    'location=Dusseldorf%2C%20Germany&location=Essen%2C%20Germany&location=Frankfurt%2C%20Germany&'
                    'location=Frankfurt%20(Oder)%2C%20Germany&location=Hamburg%2C%20Germany&location=Hannover%2C%20Germany&'
                    'location=Heidelberg%2C%20Germany&location=Karlsruhe%2C%20Germany&location=K%C3%B6ln%2C%20Germany&'
                    'location=Leipzig%2C%20Germany&location=Munich%2C%20Germany&location=Stuttgart%2C%20Germany&'
                    'page={}&descending=True')
    return url_template.format(page_num)

def fetch_jobs_data(url, headers):
    """
    Fetch job data from the given URL.

    :param url: URL to send the request to.
    :param headers: Dictionary of HTTP headers.
    :return: JSON data or None if request fails.
    """
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_job_details(job):
    """
    Parse details from a single job entry.

    :param job: Dictionary containing job details.
    :return: Dictionary with extracted and formatted job details.
    """
    html_content = BeautifulSoup(job.get('contents', ''), 'html.parser')
    
    job_info = {
        'Job Title': job.get('name'),
        'Company Name': job.get('company').get('name'),
        'Location': ', '.join([loc.get('name') for loc in job.get('locations', [])]),
        'Publication Date': job.get('publication_date'),
        'Categories': ', '.join([cat.get('name') for cat in job.get('categories', [])]),
        'Experience Level': ', '.join([level.get('name') for level in job.get('levels', [])]),
        'Job Link': job.get('refs').get('landing_page')
    }

    full_part_time_tag = html_content.find('b', string='Full / Part time:')
    if full_part_time_tag:
        job_info['Full/Part Time'] = full_part_time_tag.next_sibling.strip()
    else:
        job_info['Full/Part Time'] = None

    return job_info

def save_to_csv(data, file_path):
    """
    Save the job data to a CSV file.

    :param data: List of dictionaries with job data.
    :param file_path: Path to save the CSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

def extract_jobs(api_key, output_file, pages=70):
    """
    Extract job listings from the Muse API and save them to a CSV file.

    :param api_key: API key for authentication.
    :param output_file: File path to save the CSV file.
    :param pages: Number of pages to fetch (default is 70).
    """
    headers = {'Authorization': api_key}
    all_job_data = []

    for page_num in range(1, pages + 1):
        url = build_url(page_num)
        data = fetch_jobs_data(url, headers)
        
        if data:
            jobs = data.get('results', [])
            for job in jobs:
                job_info = parse_job_details(job)
                all_job_data.append(job_info)
        else:
            print(f"Failed to retrieve data from the URL: {url}")

    save_to_csv(all_job_data, output_file)

if __name__ == "__main__":
    api_key = load_api_key()
    extract_jobs(api_key, './data/muse/job_listings_muse_first_page1.csv')
