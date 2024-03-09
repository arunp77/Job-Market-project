#!/usr/bin/env python3
# ES load data
# Name : BS,  version: 1  Date : 20240303
# Query Elasticsearch database for analyse
# Run Docker compose and db_connection before usecase
from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib.pyplot as plt

#create the db connection
def db_connection():
    es = Elasticsearch("http://localhost:9200")
    return es

# Table name as job_list
index_name = "job_list"

# Define the search query
def usecase1():
    query = {
        "aggs": {
            "job_posted_counts": {
                "terms": {
                    "field": "job_posted",
                    "size": 200
                },
                "aggs": {
                    "data_engineer_count": {
                        "filter": {
                            "match": {
                                "title": "Data Engineer"
                            }
                        }
                    },
                    "data_scientist_count": {
                        "filter": {
                            "match": {
                                "title": "Data Scientist"
                            }
                        }
                    },
                    "machine_learning_count": {
                        "filter": {
                            "match": {
                                "title": "Machine Learning"
                            }
                        }
                    },
                    "data_analyst_count": {
                        "filter": {
                            "match": {
                                "title": "Data Analyst"
                            }
                        }
                    }
                }
            }
        }
    }
    return query


def handler():

    try:
        es = db_connection()

        query = usecase1()
        # Execute the search query
        response = es.search(index=index_name, body=query)

        # Print the response
        anayl_data = response["aggregations"]["job_posted_counts"]["buckets"]

        print(anayl_data)

        # Convert JSON data to DataFrame
        df = pd.json_normalize(anayl_data)

        # Selecting desired columns
        col = ['key_as_string', "data_analyst_count.doc_count", "data_scientist_count.doc_count",
               "data_engineer_count.doc_count", 'machine_learning_count.doc_count']

        df = df[col]
        result_df = df.copy()

        result_df.rename(columns={'key_as_string': 'job_posted',
                                  'data_analyst_count.doc_count': 'data_analyst_count',
                                  'data_scientist_count.doc_count': 'data_scientist_count',
                                  'data_engineer_count.doc_count': 'data_engineer_count',
                                  'machine_learning_count.doc_count': 'machine_learning_count'}, inplace=True)

        result_df['job_posted'] = pd.to_datetime(result_df['job_posted'])

        result_df['job_posted'] = result_df['job_posted'].dt.strftime('%Y-%m-%d')

        # Print the resulting DataFrame
        print(len(result_df))
        print(result_df.head())
        # Plot trend of job postings over time
        plt.figure(figsize=(10, 6))
        plt.plot(result_df['job_posted'], result_df['data_analyst_count'] , label='data_analyst_count')
        plt.plot(result_df['job_posted'],   result_df['data_engineer_count'] ,label='data_engineer_count')
        plt.plot(result_df['job_posted'],  result_df['data_scientist_count'] ,label='data_scientist_count')
        plt.plot(result_df['job_posted'], result_df['machine_learning_count'], label='machine_learning_count')
        plt.xlim(result_df['job_posted'].min(), result_df['job_posted'].max())
        plt.xlabel('Date')
        plt.ylabel('Count of Job')
        plt.title('Trend of Job Postings Over Time')
        plt.legend()
        plt.grid(True)
        plt.show()

    except Exception as e:
        print(f"An unexpected error occurred in the main block: {e}")
        raise

# call mainfuntion handler to execute
if __name__ == "__main__":

    handler()
