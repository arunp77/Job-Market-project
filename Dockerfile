# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .


# Expose ports for FastAPI (8000), Elasticsearch (9200), and Kibana (5601)
# Note: Exposing ports in a Dockerfile does not publish them to the host machine
# This only serves as documentation for users of the image

# 1. Expose port 8000 for FastApi to allow external access
EXPOSE 8000

# 2. Expose port 9200 for Elasticsearch to allow external access
EXPOSE 9200

# 3. Expose port 9200 for Kibana to allow external access
EXPOSE 5601

# Run script or command to start the application
CMD ["python", "api.py"]

## will run it for running complete project at once
# CMD ["python", "api.py"]