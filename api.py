from fastapi import FastAPI
from scripts.database.db_connection import db_connection, ss_dataset, adzuna_dataset, muse_dataset
from scripts.plot_analyse import usecase,  computation

import os
import pandas as pd

api = FastAPI(
    title="Job Market API",
    description="API powered by FastAPI for our project.",
    version="1.0.1",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Create a global Elasticsearch connection
es = db_connection()
index_name = "job_list"

@api.get("/")
def read_root():
    """Root endpoint to welcome users."""
    return {"message": "Welcome to the Job Market API!"}

@api.get("/load_data")
def load_data():
    """Endpoint to load data into Elasticsearch."""
    try:
        # Get the absolute path of the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the processed_data directory
        read_file_path = os.path.join(current_dir, "data", "processed_data")
        
        ss_result = ss_dataset(read_file_path, es)
        adzuna_result = adzuna_dataset(read_file_path, es)
        muse_result = muse_dataset(read_file_path, es)
        
        return {
            "ss_result": ss_result,
            "adzuna_result": adzuna_result,
            "muse_result": muse_result
        }
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An unexpected error occurred: {str(e)}")
        # Return a more specific error message
        return {"error": "Failed to load data into Elasticsearch."}
    
    
@api.get("/usecase1")
def get_usecase1():
    """Endpoint to execute and retrieve results for use case 1."""
    try:
        host = "localhost"
        port = "9200"
        # Connect to Elasticsearch
        es = db_connection(host, port)
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

@api.get("/usecase2")
def get_usecase2():
    """Endpoint to execute and retrieve results for use case 2."""
    try:
        host = "localhost"
        port = "9200"
        # Connect to Elasticsearch
        es = db_connection(host, port)
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
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)