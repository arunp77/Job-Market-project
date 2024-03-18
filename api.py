from fastapi import FastAPI
from scripts.database.db_connection import db_connection, ss_dataset, adzuna_dataset, muse_dataset

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)