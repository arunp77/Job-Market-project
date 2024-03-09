#!/usr/bin/env python3
# ES load data
# Name : BS,  version: 1  Date : 20240227
# Code is to load data to Elasticsearch database
# Todo In the docker need to add credetials.

from elasticsearch import Elasticsearch
import pandas as pd
import logging
import os

logging.basicConfig(filename='logfile.log', level=logging.DEBUG)

# Table name as job_list
index_name = "job_list"
# table schema structure
mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},  # Unique ID field
            "title": {"type": "text"},
            "company": {"type": "text"},
            "location": {"type": "text"},
            "job_posted": {"type": "date"},
            "categories": {"type": "text"},
            "experience_level": {"type": "text"},
            "full_part_time": {"type": "text"},
            "description": {"type": "text"},
            "link": {"type": "text"},
            "source": {"type": "text"}

        }
    }
}


#create the db connection
def db_connection():
    es = Elasticsearch("http://localhost:9200")
    return es


# load the muse dataset to elastic search
"""
GET /job_list/_search
{
  "query": {
    "term": {
        "source": "muse"
    }
  }
}"""
def muse_dataset(filepath,es):
    df_final = pd.DataFrame()
    filepath = os.path.join(filepath, "muse_processed_data")
    files = [f for f in os.listdir(filepath) if f.lower().endswith('.csv')]
    for file in files:
        filepath_1 = os.path.join(filepath, file)
        print(filepath_1)
        df = pd.read_csv(filepath_1)
        df_final = pd.concat([df,df_final])
        print(len(df_final))
    for _, row in df_final.iterrows():
        doc = {
            "title": row["Job Title"],
            "company": row["Company Name"],
            "location": row["Location"],
            "job_posted": row["Publication Date"],
            "categories": row["Categories"],
            "experience_level": row["Experience Level"],
            "full_part_time": row["Full/Part Time"],
            "link": row["Job Link"],
            "source": "muse"
        }
        es.index(index=index_name, body=doc)
    return "Execution Sucess"

"""
GET /job_list/_search
{
  "query": {
    "term": {
        "source": "adzuna"
    }
  }
}"""


# load the adzuna dataset to elastic search
def adzuna_dataset(filepath,es):
    df_final = pd.DataFrame()
    filepath = os.path.join(filepath, "adjurna_processed_data")
    files = [f for f in os.listdir(filepath) if f.lower().endswith('.csv')]
    # loop to get all the csv files in the path to a single datafrane
    for file in files:
        filepath_1 = os.path.join(filepath, file)
        print(filepath_1)
        df = pd.read_csv(filepath_1)
        df_final = pd.concat([df,df_final])
        print(len(df_final))

    # check the data quanlity and take care of this step in the ETL part

    df_final = df_final.drop(columns=['description'])
    df_final = df_final.rename(columns={'category': 'description'})
    df_final = df_final.rename(columns={'category': 'description'})

    for _, row in df_final.iterrows():
        doc = {
            "title": row["title"],
            "company": row["company"],
            "location": row["location"],
            "job_posted": row["job_posted"],
            #"categories": row["category"],
            "description": row["description"],
            "link": row["link"],
            "source": "adzuna"
        }
        es.index(index=index_name, body=doc)
    return "Execution Sucess"


"""
GET /job_list/_search
{
  "query": {
    "term": {
        "source": "stepstone"
    }
  }
}"""
# load stepstone dataset
def ss_dataset(filepath,es):
    df_final = pd.DataFrame()
    filepath = os.path.join(filepath, "ss_processed_data")
    files = [f for f in os.listdir(filepath) if f.lower().endswith('.csv')]
    # loop to get all the csv files in the path to a single datafrane

    for file in files:
        filepath_1 = os.path.join(filepath, file)
        print(filepath_1)
        df = pd.read_csv(filepath_1)
        df_final = pd.concat([df,df_final])
        print(len(df_final))
    for _, row in df_final.iterrows():
        doc = {
            "title": row["title"],
            "company": row["company"],
            "location": row["location"],
            "job_posted": row["job_posted"],
            "link": row["link"],
            "source": "stepstone"
        }
        es.index(index=index_name, body=doc)
    return "Execution Sucess"


def handler():

    try:
        # extablsh db connection to the variable es.
        es = db_connection()
        print(es.info().body)
        # Check if index(table) exists
        if not es.indices.exists(index=index_name):
            # Create index(table) with mapping
            es.indices.create(index=index_name, body=mapping)
            print(f"Index '{index_name}' created successfully.")
        else:
            es.indices.delete(index=index_name)
            print(f"Index '{index_name}' already exists. so drop and create new")

        # get script base path
        script_dir = os.path.dirname(os.path.realpath(__file__))
        read_file_path = script_dir.replace("\scripts\database", "\data\processed_data")
        print(read_file_path)
        # call the below function to load the dataset successfully to ES database
        ss_dataset(read_file_path, es)
        adzuna_dataset(read_file_path, es)
        muse_dataset(read_file_path, es)


    except Exception as e:
        print(f"An unexpected error occurred in the main block: {e}")
        raise

# call mainfuntion handler to execute
if __name__ == "__main__":

    handler()
