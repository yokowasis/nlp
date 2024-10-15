# Use the official Python 3.10.14 image from the Docker Hub
FROM python:3.10.14-slim

# Set the working directory in the container
WORKDIR /app

EXPOSE 8080

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files (optional)
COPY . /app

# Command to run your application using Waitress
CMD ["waitress-serve", "--host", "localhost", "--port","8080", "backend:app"]