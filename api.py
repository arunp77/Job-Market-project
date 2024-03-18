from fastapi import FastAPI
from scripts.database import db_connection

app = FastAPI()

# Define API endpoints
@app.get("/load_data")
def load_data():
    # Call your data loading function from db_connection.py
    # For example:
    # db_connection.load_data()
    return {"message": "Data loaded successfully"}

@app.get("/analyze_data")
def analyze_data():
    # Call your data analysis function from scripts.plot_analysis.uscase.py
    # For example:
    # uscase.analyze_data()
    return {"message": "Data analysis completed"}

# Add more endpoints as needed

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
