FROM python:3.9-slim

LABEL authors="Kevin"

WORKDIR /app

COPY . /app
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# environment variables
ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_USER=postgres
ENV DB_PASSWORD=admin
ENV DB_NAME=postgres


RUN python create_db.py


CMD ["python", "crud_services.py"]
