# Use an official Python runtime as a parent image
FROM python:3.12-bookworm

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

RUN pip install playwright==@1.43.0 && \
    playwright install --with-deps

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Command to run the FastAPI application with Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]