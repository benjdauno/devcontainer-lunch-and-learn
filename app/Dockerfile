FROM python:3.10-slim

WORKDIR /app

# Install dependencies for database connectivity
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install pymysql
RUN pip install pymysql flask

# Command to keep the container running
CMD ["python", "app.py"]
