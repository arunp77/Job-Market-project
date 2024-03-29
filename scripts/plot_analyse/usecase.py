#!/usr/bin/env python3
# ES load data
# Name : BS,  version: 2  Date : 20240303
# Query Elasticsearch database for analyse
# Run Docker compose and db_connection before usecase
from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
import plotly.graph_objs as go
import plotly.express as px
from plotly.offline import plot


#create the db connection
def db_connection(host,port):
    es = Elasticsearch(f"http://{host}:{port}")
    return es


# Table name as job_list
index_name = "job_list"


""" 
    Define the serach query for analytical
    usecase 1:
    get the count of the job opening for Data Engineer, Data Scientist, Machine Learning and Data Analyst per day in the given dataset
    This will provide trend of job postings over time
    Usecase 2:
    get the top 10 maximum job posted companies to understand the companies which has max opening in the dataset 
"""

def usecase(usecase):
    if usecase == 1:
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
    elif usecase == 2:
        query = {
              "size": 0,
              "aggs": {
                "unique_jobs": {
                  "composite": {
                    "size": 10000,
                    "sources": [
                      { "title": { "terms": { "field": "title.keyword" }}},
                      { "company": { "terms": { "field": "company.keyword" }}}
                    ]
                  }
                },
                "companies": {
                  "terms": {
                    "field": "company.keyword",
                    "size": 10,
                    "order": { "_count": "desc" }
                  }
                }
              }
            }

    return query


""" 
The dataframe need to be transform based on the analytical need.
We receive data from elastic search as json. Load to the Dataframe and get the required field with suitable titles for each use cases
"""

def computation(usecase, df):
    if usecase == 1:
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
    elif usecase == 2:

        # Selecting desired columns
        col = ['key', "doc_count"]

        df = df[col]
        result_df = df.copy()

        result_df.rename(columns={'key': 'company',
                                  'doc_count': 'job_counts'}, inplace=True)
    return result_df


""" 
    Plot each usecase to understand better in plots
    usecase 1:
    line chart to understand the trend of job postings for each fields in Data Science 
    (Data Engineer, Data Scientist, Machine Learning and Data Analyst) over time
    Usecase 2:
        pie chart for the top 10 maximum job posted companies to understand the companies 
"""
def plot_trend(result_df_1,result_df_2):
    # Plot trend of job postings over time
    plt.figure(figsize=(25, 10))
    # subplot 1
    plt.subplot(121)
    plt.plot(result_df_1['job_posted'], result_df_1['data_analyst_count'], label='Data Analyst')
    plt.plot(result_df_1['job_posted'], result_df_1['data_engineer_count'], label='Data Engineer')
    plt.plot(result_df_1['job_posted'], result_df_1['data_scientist_count'], label='Data Scientist')
    plt.plot(result_df_1['job_posted'], result_df_1['machine_learning_count'], label='Machine Learning')
    plt.xlim(result_df_1['job_posted'].min(), result_df_1['job_posted'].max())
    plt.ylim(result_df_1['data_engineer_count'].min(), 30)
    plt.xlabel('Date')
    plt.ylabel('Count of Job')
    plt.title('Trend of Job Postings Over Time')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility
    plt.legend()
    #plt.grid(True)

    # subplot 2
    plt.subplot(122)
    # Create pie chart to get the highest job opening for 10 companies
    plt.pie(result_df_2['job_counts'], labels=result_df_2['company'], autopct='%1.1f%%', startangle=140)
    plt.title('Job Counts by Company')
    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')

    return plt


def plot_trend_interactive(result_df_1, result_df_2):
    # creating the time series plot
    result_df_1 = result_df_1.sort_values("job_posted").reset_index(drop=True)
    #result_df_1['job_posted'] = pd.to_datetime(result_df_1['job_posted'])
    print(result_df_1['job_posted'])
    fig = go.Figure()

    # Adding the traces for each job category
    fig.add_trace(go.Scatter(x=result_df_1['job_posted'], y=result_df_1['data_analyst_count'], mode='lines', name='Data Analyst'))
    fig.add_trace(go.Scatter(x=result_df_1['job_posted'], y=result_df_1['data_engineer_count'], mode='lines', name='Data Engineer'))
    fig.add_trace(go.Scatter(x=result_df_1['job_posted'], y=result_df_1['data_scientist_count'], mode='lines', name='Data Scientist'))
    fig.add_trace(go.Scatter(x=result_df_1['job_posted'], y=result_df_1['machine_learning_count'], mode='lines', name='Machine Learning'))
    x_min_limit = result_df_1['job_posted'].min()
    x_max_limit = result_df_1['job_posted'].max()
    y_min_limit = 0
    y_max_limit = 30
    # Updating the layout for time series
    fig.update_layout(
        title='Trend of Job Postings Over Time',
        xaxis_title='Date',
        yaxis_title='Count of Job',
        xaxis=dict(tickangle=-45, range=[x_min_limit, x_max_limit]),
        yaxis=dict(range=[y_min_limit, y_max_limit]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=60, b=20),
        hovermode='x unified'
    )


    # Pie plot creating now
    fig_pie = go.Figure()

    # Adding pie chart for top 10 companies
    fig_pie.add_trace(go.Pie(labels=result_df_2['company'], values=result_df_2['job_counts'], hole=0.3))

    # Update layout for pie plot
    fig_pie.update_layout(
        title='Job Counts by Company'
    )

    return fig, fig_pie


#main funtions
def handler():

    try:
        host  = "localhost"
        port = "9200"
        # connect to DB
        es = db_connection(host,port)
        # usecase 1 execution
        query = usecase(usecase=1)
        # Execute the search query and get the response
        response = es.search(index=index_name, body=query)
        # get the required data
        anayl_data = response["aggregations"]["job_posted_counts"]["buckets"]
        # Convert JSON data to DataFrame and do the computation
        df = pd.json_normalize(anayl_data)
        result_df_1 = computation(usecase=1, df=df)
        # usecase 2 execution
        query = usecase(usecase=2)
        # Execute the search query and get the response
        response = es.search(index=index_name, body=query)
        # get the required data
        anayl_data = response["aggregations"]["companies"]["buckets"]
        # Convert JSON data to DataFrame and do the computation
        df = pd.json_normalize(anayl_data)
        result_df_2 = computation(usecase=2, df=df)

        # for save the plot over time get the timestamp in numerical part
        unix_timestamp = int(time.time())
        # prepare path to save
        script_dir = os.path.dirname(os.path.realpath(__file__))
        plt_file_path = script_dir.replace("\scripts\plot_analyse", "\data\plot")
        plot_file = os.path.join(plt_file_path, f"job_analyse_postings_{unix_timestamp}.png")
        # prepare plot
        plot_dia = plot_trend(result_df_1,result_df_2)
        # save plot in a file path
        plot_dia.savefig(plot_file)

        # get interactive plot results and save in html files
        plot_dia_i1,plot_dia_i2 = plot_trend_interactive(result_df_1,result_df_2)
        plot_file = os.path.join(plt_file_path, f"job_analyse_tend_{unix_timestamp}.html")
        plot_dia_i1.write_html(plot_file)
        plot_file = os.path.join(plt_file_path, f"job_analyse_max_job_{unix_timestamp}.html")
        plot_dia_i2.write_html(plot_file)

    except Exception as e:
        print(f"An unexpected error occurred in the main block: {e}")
        raise


# call main funtion handler to execute
if __name__ == "__main__":

    handler()
