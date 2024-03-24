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

