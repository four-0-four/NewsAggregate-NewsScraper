# Use a smaller base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Update package list and install necessary dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*


RUN python -m pip install --no-cache-dir virtualenv

RUN python -m virtualenv myvenv

RUN . myvenv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

#### NOTE: we need to activate the virtual environment before each important command
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
