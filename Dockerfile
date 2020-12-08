FROM python:3.7.2-stretch

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/requirements.txt

# Install the dependencies
RUN apt-get update
RUN pip install -r requirements.txt

# Copy source code
ADD . /app
