# Use the Playwright base image
FROM ubuntu:20.04

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Update package list, add the deadsnakes PPA, and install necessary dependencies, including Python 3.11 and pip
RUN apt update \
    && apt install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt update \
    && apt install -y python3.11 \
    && apt install -y python3.11-distutils \
    && apt install -y curl \
    && curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3.11 get-pip.py

# Install virtualenv
RUN python3.11 -m pip install virtualenv

# Create and activate a virtual environment
RUN python3.11 -m virtualenv myvenv

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
CMD ["sh", "-c", ". myvenv/bin/activate && uvicorn api:app --host 0.0.0.0 --port 8000"]
