# Use a smaller base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Update package list and install necessary dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install virtualenv
RUN python -m pip install --no-cache-dir virtualenv

# Create and activate a virtual environment
RUN python -m virtualenv myvenv

# Activate virtual environment and install Python dependencies
RUN . myvenv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

# Install Playwright and its dependencies
RUN . myvenv/bin/activate \
    && pip install playwright \
    && playwright install-deps \
    && playwright install --with-deps

# Expose port 8000 to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Command to run the FastAPI application with Uvicorn
#CMD ["sh", "-c", ". myvenv/bin/activate && uvicorn api:app --host 0.0.0.0 --port 8000"]
