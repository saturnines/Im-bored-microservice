# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API Gateway service files into the container
COPY api_gateway_service/ .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the API Gateway service
CMD ["python", "api_gateway.py"]