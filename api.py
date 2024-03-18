from fastapi import FastAPI
from elasticsearch import Elasticsearch
import os
import pandas as pd

app = FastAPI()

# Database configuration
es = Elasticsearch("http://localhost:9200")
index_name = "job_list"

# Load dataset endpoints: here '/load_muse_dataset' is the endpoint
@app.get("/load_muse_dataset")
def load_muse_dataset():
    try:
        df = pd.read_csv("data/processed_data/muse_processed_data.csv")
        for _, row in df.iterrows():
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
        return {"message": "Muse dataset loaded successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/load_adzuna_dataset")
def load_adzuna_dataset():
    try:
        df = pd.read_csv("data/processed_data/adzuna_processed_data.csv")
        for _, row in df.iterrows():
            doc = {
                "title": row["title"],
                "company": row["company"],
                "location": row["location"],
                "job_posted": row["job_posted"],
                "description": row["description"],
                "link": row["link"],
                "source": "adzuna"
            }
            es.index(index=index_name, body=doc)
        return {"message": "Adzuna dataset loaded successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/load_adzuna_dataset")
def load_adzuna_dataset():
    try:
        df = pd.read_csv("data/processed_data/adjurna_processed_data.csv")
        for _, row in df.iterrows():
            doc = {
                "title": row["title"],
                "company": row["company"],
                "location": row["location"],
                "job_posted": row["job_posted"],
                "link": row["link"],
                "source": "adzuna"
            }
            es.index(index=index_name, body=doc)
        return {"message": "Adzuna dataset loaded successfully"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
