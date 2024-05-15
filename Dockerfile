# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install missing system dependencies
RUN apt-get update && \
    apt-get install -y \
    libicu66 \
    libevent-2.1-7 \
    libjpeg8 \
    libenchant-2-2 \
    libsecret-1-0 \
    libffi7 \
    libgles2 || apt-get install -y libicu-dev

# Install Playwright browsers
RUN playwright install

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run main.py when the container launches
CMD ["python", "main.py"]
