# Use an official Python runtime as a parent image
FROM python:3.13.0a4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8081

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the application
CMD python3 manage.py 8081