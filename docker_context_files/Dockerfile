
FROM python:3.9-slim

# Set Dir
WORKDIR /app

# Copy Dir
COPY . /app

# Install Packages
RUN pip install --no-cache-dir -r requirements.txt


ENV PYTHONPATH=/app

# Different Ports. Change if you mess with the flask ports too.
EXPOSE 5000 5001 5002

# Run the services
CMD ["sh", "-c", "python api_gateway.py & python user_auth.py & python crud_services.py"]