from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase
from bson import ObjectId
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

import os
import pandas as pd
import uvicorn
from scripts.plot_analyse.usecase import usecase, handler
from scripts.database.db_connection import db_connection, ss_dataset, adzuna_dataset, muse_dataset
from scripts.plot_analyse.usecase import computation

# Initialize FastAPI
app = FastAPI(
    title="Job Market API",
    description="API powered by FastAPI for our project. This project aims to gather, process, create a database and deploy using FASTApi. By the end of the project, we aim to have a clearer understanding of the job market, including sectors with the highest demand, required skills, active cities, and more.",
    version="1.0.1",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["fastapi_users_demo"]

# Define MongoDB user collection
users_collection = db["users"]

# Define MongoDB user database
user_db = MongoDBUserDatabase(models.UserDB, users_collection)

# Define JWT secret key
SECRET_KEY = "secret"

# Define JWT authentication
auth_backends = [JWTAuthentication(secret=SECRET_KEY, lifetime_seconds=3600)]

# Define OAuth2 password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define user roles
class UserRole(models.Role):
    ADMIN = "admin"
    USER = "user"

# Define user model
class User(models.BaseUser):
    role: UserRole

# Define user create model
class UserCreate(models.BaseUserCreate):
    role: UserRole

# Define user update model
class UserUpdate(User, models.BaseUserUpdate):
    pass

# Define user DB model
class UserDB(User, models.BaseUserDB):
    pass

# Initialize FastAPI users
fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

# CORS (Cross-Origin Resource Sharing) settings
origins = [
    "http://localhost",
    "http://localhost:8000",
]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Rate limiting settings
limiter = FastAPILimiter(
    key_func=lambda _: "global",
    rate_limit=100,
    per_second=10,
)

# Rate limiter middleware
app.add_middleware(RateLimiter, limiter=limiter)

# Secure headers middleware
@app.middleware("http")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

# Example model for data input validation
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# Example endpoint with input validation
@app.post("/items/")
async def create_item(item: Item):
    return item

# Endpoint to get token
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await fastapi_users.get_authenticator().get_login_response(form_data)

# Endpoint to get current user
@app.get("/users/me")
async def read_users_me(current_user: UserDB = Depends(fastapi_users.get_current_active_user)):
    return current_user

# Endpoint to create new user
@app.post("/users/", response_model=UserDB)
async def create_user(user: UserCreate):
    return await fastapi_users.create_user(user)

# Example of protected endpoint that requires authentication and admin role
@app.get("/admin/")
async def admin_protected_endpoint(current_user: UserDB = Depends(fastapi_users.get_current_active_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not have admin role")
    return {"message": "Welcome to the admin area!"}

# Example of protected endpoint that requires authentication only
@app.get("/user/")
async def user_protected_endpoint(current_user: UserDB = Depends(fastapi_users.get_current_active_user)):
    return {"message": "Welcome to the user area!"}

# Example of logging
import logging

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

# Example of monitoring
from prometheus_client import Counter
from fastapi import Request
from starlette_exporter import PrometheusMiddleware, handle_metrics

request_counter = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint"])

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    request_counter.labels(method=request.method, endpoint=request.url.path).inc()
    response = await call_next(request)
    return response

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", handle_metrics)

# Create a global Elasticsearch connection
es = db_connection()
"""_summary_
Elasticsearch serves as the data store and querying engine for our use case endpoints 
(get_usecase1 and get_usecase2). so keeping it here.
Returns:
    _type_: _description_
"""

index_name = "job_list"

@app.get("/", description="Root endpoint to welcome users.")
def welcome():
    """Root endpoint to welcome users."""
    return {"message": "Welcome to the Job Market API!"}


# Create API endpoints to trigger the use cases
@app.get("/load_data", description="Endpoint to load data into Elasticsearch.")
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

@app.get("/usecase1", description="Endpoint to execute and retrieve results for use case 1 and it gives the distribution of job postings over time for specific job titles, including Data Engineer, Data Scientist, Machine Learning, and Data Analyst.")
def get_usecase1():
    """Endpoint to execute and retrieve results for use case 1 and it gives the distribution of job postings over time for specific job titles, including Data Engineer, Data Scientist, Machine Learning, and Data Analyst."""
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
    
@app.get("/usecase2", description="Endpoint to execute and retrieve results for use case 2 and finds the most common job titles and companies in the dataset.")
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

@app.get("/thank-you", description="Thank you for using the Job Market API! We hope you found it helpful..")
def thank_you():
    """Endpoint to display a thank you message."""
    return {"message": "Thank you for using the Job Market API! We hope you found it helpful."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
