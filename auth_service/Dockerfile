LABEL authors="Kevin"
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
ENV SECRET_KEY=5f4102db508e4065ace3df7ae799f6cf

#init db
RUN python create_db.py

# Open Port
EXPOSE 5001


CMD ["python", "user_auth.py"]
