# Layer 1
# Use an official Python runtime as a parent image
FROM python:3.10

# Layer 2
# Copy the current directory contents into the container at /app
COPY requirements.txt /app/

# Layer 3
# Copy the requirements file to the working directory
#COPY requirements.txt .

# Layer 4
# Set the working directory in the container
WORKDIR /app

# Layer 5
# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Layer 6
# Copy the entire project directory into the container
COPY . /app/

# Layer 7
# Expose ports for FastAPI (8000), Elasticsearch (9200), and Kibana (5601)
# Note: Exposing ports in a Dockerfile does not publish them to the host machine
# This only serves as documentation for users of the image 

# Layer 8
# 1. Expose port 8000 for FastApi to allow external access
EXPOSE 8000

# Layer 9
# 2. Expose port 9200 for Elasticsearch to allow external access
EXPOSE 9200

# Layer 10
# 3. Expose port 9200 for Kibana to allow external access
EXPOSE 5601

# Layer 11
# Run script or command to start the application
# ENTRYPOINT ["python", "api.py"]
CMD ["python", "api.py"]