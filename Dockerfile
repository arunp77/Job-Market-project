# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the GPG key as an environment variable (optional)
ENV GPG_KEY=$GPG_KEY

# Run script or command to start your application
CMD ["python", "scripts/etl/etl_script.py"]
