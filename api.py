from fastapi import FastAPI 
import uvicorn
from scripts.plot_analyse.usecase import usecase, handler
from scripts.database.db_connection import db_connection, ss_dataset, adzuna_dataset, muse_dataset
from scripts.plot_analyse.usecase import computation

import os
import pandas as pd

api = FastAPI(
    title="Job Market API",
    description="API powered by FastAPI for our project. This project aims to gather, process, create a database and deploy using FASTApi. By the end of the project, we aim to have a clearer understanding of the job market, including sectors with the highest demand, required skills, active cities, and more.",
    version="1.0.1",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Create a global Elasticsearch connection
es = db_connection()
"""_summary_
Elasticsearch serves as the data store and querying engine for our use case endpoints 
(get_usecase1 and get_usecase2). so keeping it here.
Returns:
    _type_: _description_
"""

index_name = "job_list"

@api.get("/", description="Root endpoint to welcome users.")
def welcome():
    """Root endpoint to welcome users."""
    return {"message": "Welcome to the Job Market API!"}


# Create API endpoints to trigger the use cases
@api.get("/load_data", description="Endpoint to load data into Elasticsearch.")
def load_data():
    """Endpoint to load data into Elasticsearch."""
    try:
        # Get the absolute path of the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the processed_data directory
        read_file_path = os.path.join(current_dir, "data", "processed_data")

        # Load data into Elasticsearch
        ss_result = ss_dataset(read_file_path, es)
        adzuna_result = adzuna_dataset(read_file_path, es)
        muse_result = muse_dataset(read_file_path, es)

        return {
            "ss_result": ss_result,
            "adzuna_result": adzuna_result,
            "muse_result": muse_result
        }
    except Exception as e:
        # Log and return error message
        print(f"An unexpected error occurred: {str(e)}")
        return {"error": "Failed to load data into Elasticsearch."}

@api.get("/usecase1", description="Endpoint to execute and retrieve results for use case 1.")
def get_usecase1():
    """Endpoint to execute and retrieve results for use case 1."""
    try:
        # Define the search query for use case 1
        query = usecase(1)
        # Execute the search query and get the response
        response = es.search(index=index_name, body=query)
        # Get the required data
        analysis_data = response["aggregations"]["job_posted_counts"]["buckets"]
        # Convert JSON data to DataFrame and perform computation
        df = pd.json_normalize(analysis_data)
        result_df = computation(1, df)
        # Return the results
        return result_df.to_dict(orient='records')
    except Exception as e:
        # Log and return error message
        print(f"An unexpected error occurred: {str(e)}")
        return {"error": "Failed to execute use case 1."}
    
@api.get("/usecase2", description="Endpoint to execute and retrieve results for use case 2.")
def get_usecase2():
    """Endpoint to execute and retrieve results for use case 2."""
    try:
        # Define the search query for use case 2
        query = usecase(2)
        # Execute the search query and get the response
        response = es.search(index=index_name, body=query)
        # Get the required data
        analysis_data = response["aggregations"]["companies"]["buckets"]
        # Convert JSON data to DataFrame and perform computation
        df = pd.json_normalize(analysis_data)
        result_df = computation(2, df)
        # Return the results
        return result_df.to_dict(orient='records')
    except Exception as e:
        # Log and return error message
        print(f"An unexpected error occurred: {str(e)}")
        return {"error": "Failed to execute use case 2."}

if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)