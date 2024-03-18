# Job Market API

Welcome to the Job Market API! This API provides functionalities to extract, transform, load (ETL), and analyze job market data from various sources. The API allows users to interact with the data stored in the system, perform ETL processes, and execute predefined use cases for data analysis.

## Installation and Setup

1. **Clone the Repository**: Clone the project repository to your local machine.
   ```
   git clone https://github.com/your_username/Job-Market-project.git
   cd Job-Market-project
   ```

2. **Install Dependencies**: Install the required Python dependencies for the project.
   ```
   pip install -r requirements.txt
   ```
   or you can also install the `FastAPI` and `uvicorn` separatly into our project enviorment:
   ```bash
   pip install fastapi uvicorn
   ```

3. **Environment Variables**: Set up any necessary environment variables, such as API keys or Elasticsearch credentials, in the `.env` file. Make sure to add this file to the `.gitignore` to avoid committing sensitive information.

4. **Run the API**: Start the FastAPI application using Uvicorn.
   ```
   uvicorn api:app --reload
   ```

## API Endpoints

- `/scraped_data`: Endpoint to trigger the data extraction and loading process.
- `/processed_data`: Endpoint to execute predefined use cases for data analysis.

## Usage

1. **Load Data**:
   ```
   GET http://localhost:8000//scraped_data
   ```

2. **Analyze Data**:
   ```
   GET http://localhost:8000//processed_data
   ```

## Additional Information

- **Error Handling:** The API returns appropriate status codes and error messages for invalid requests or errors.
- **Authentication:** Add authentication mechanisms to restrict access to sensitive endpoints.
- **Rate Limiting:** Implement rate limiting to prevent abuse of the API.
