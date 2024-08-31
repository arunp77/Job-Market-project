import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_api_key(env_var_name):
    """
    Load the API key from an environment variable.

    :param env_var_name: Name of the environment variable containing the API key.
    :return: The API key as a string.

    >>> load_api_key('API_KEY1') is not None
    True
    """
    return os.getenv(env_var_name)

def build_url(page_num):
    """
    Build the API request URL for a given page number.

    :param page_num: Page number to request.
    :return: A formatted URL string.
    
    >>> build_url(1).startswith("https://www.themuse.com/api/public/jobs")
    True
    >>> "page=1" in build_url(1)
    True
    """
    url_template = ('https://www.themuse.com/api/public/jobs?category=Computer%20and%20IT&category=Data%20and%20Analytics'
                    '&category=Data%20Science&category=IT&level=Entry%20Level&level=Mid%20Level&level=Senior%20Level'
                    '&level=management&location=Berlin%2C%20DE&location=Berlin%2C%20Germany&location=Cologne%2C%20Germany'
                    '&location=Dusseldorf%2C%20Germany&location=Essen%2C%20Germany&location=Frankfurt%2C%20Germany'
                    '&location=Frankfurt%20(Oder)%2C%20Germany&location=Hamburg%2C%20Germany&location=Hannover%2C%20Germany'
                    '&location=Heidelberg%2C%20Germany&location=Karlsruhe%2C%20Germany&location=K%C3%B6ln%2C%20Germany'
                    '&location=Leipzig%2C%20Germany&location=Munich%2C%20Germany&location=Stuttgart%2C%20Germany&page={}'
                    '&descending=True')
    return url_template.format(page_num)

def fetch_jobs_data(url, headers):
    """
    Fetch jobs data from the API.

    :param url: The API URL to request.
    :param headers: Dictionary containing request headers, including the API key.
    :return: Parsed JSON data from the API response.

    >>> headers = {'Authorization': 'dummy_api_key'}
    >>> isinstance(fetch_jobs_data(build_url(1), headers), dict)
    True
    """
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data from the URL:", url)
        return {}

def parse_job_details(job):
    """
    Parse details from a single job entry.

    :param job: Dictionary containing job details.
    :return: Dictionary with extracted and formatted job details.
    
    >>> job = {
    ...     'name': 'Data Scientist',
    ...     'company': {'name': 'Tech Corp'},
    ...     'locations': [{'name': 'Berlin, Germany'}],
    ...     'publication_date': '2024-01-01',
    ...     'categories': [{'name': 'Data Science'}],
    ...     'levels': [{'name': 'Mid Level'}],
    ...     'refs': {'landing_page': 'https://example.com/job'}
    ... }
    >>> job_info = parse_job_details(job)
    >>> job_info['Job Title']
    'Data Scientist'
    >>> job_info['Company Name']
    'Tech Corp'
    >>> job_info['Location']
    'Berlin, Germany'
    >>> job_info['Categories']
    'Data Science'
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

    :param data: List of dictionaries containing job details.
    :param file_path: Path to the output CSV file.
    
    >>> data = [{'Job Title': 'Data Scientist'}]
    >>> save_to_csv(data, 'dummy_path.csv')  # doctest: +SKIP
    """
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

if __name__ == "__main__":
    api_key = load_api_key("API_KEY1")
    headers = {'Authorization': api_key}

    all_job_data = []

    for page_num in range(1, 71):
        url = build_url(page_num)
        data = fetch_jobs_data(url, headers)
        jobs = data.get('results', [])
        
        for job in jobs:
            job_info = parse_job_details(job)
            all_job_data.append(job_info)

    save_to_csv(all_job_data, './data/muse/job_listings_muse_first_page1.csv')
