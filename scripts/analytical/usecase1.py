from elasticsearch import Elasticsearch
import pandas as pd

# Create an Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# Define the search query
query = {
    "aggs": {
        "job_posted_counts": {
            "terms": {
                "field": "job_posted",
                "size": 2000
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

# Execute the search query
response = es.search(index='job_list', body=query)

# Print the response
anayl_data = response["aggregations"]["job_posted_counts"]["buckets"]

print(anayl_data)

# Convert JSON data to DataFrame
df = pd.json_normalize(anayl_data)

# Selecting desired columns
col = ['key_as_string', "data_analyst_count.doc_count" ,"data_scientist_count.doc_count",
                    "data_engineer_count.doc_count", 'machine_learning_count.doc_count']


result_df = df[col]

result_df.rename(columns={'data_analyst_count.doc_count': 'data_analyst_count',
                          'data_scientist_count.doc_count': 'data_scientist_count',
                          'data_engineer_count.doc_count': 'data_engineer_count',
                          'machine_learning_count.doc_count': 'machine_learning_count' }, inplace=True)

# Print the resulting DataFrame
print(len(result_df))
print(result_df.head())

