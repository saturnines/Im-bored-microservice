# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the Python path to include the current directory
ENV PYTHONPATH=/app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the services when the container launches
CMD ["sh", "-c", "python api_gateway.py & python user_auth.py & python crud_services.py"]