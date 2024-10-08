# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables to prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Set environment variable to buffer output, useful for debugging
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the .env file into the container
COPY .env /app/.env

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Expose the port the app runs on
EXPOSE 5001

# Define the command to run the app
CMD ["python", "app.py"]
