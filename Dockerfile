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

# Expose port 8000 to allow external access
EXPOSE 8000

# Run script or command to start your application
CMD ["python", "scripts/etl/etlscript.py"]
# CMD ["python", "api.py"] # will run it for running complete project at once
