# Use the official Python 3.10.14 image from the Docker Hub
FROM python:3.10.14-slim

# Install PostgreSQL development package
RUN apt-get update && \
    apt-get install -y libpq-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

EXPOSE 3000

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files (optional)
COPY . /app

# Command to run your application using Waitress
CMD ["python", "serve-flask.py"]