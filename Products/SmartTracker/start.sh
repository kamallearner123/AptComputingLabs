# Configuration
#!/bin/bash
# This script is used to start the Django server for the Smart Tracker project.
# Make sure to set the correct environment variables for your Django project.
SERVER_IP="0.0.0.0"
SERVER_PORT="8090"
export POSTGRES_PASSWORD="postgres@123"
export POSTGRES_USER="postgres"
export POSTGRES_DB="tracker_db_recent"
export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5432"

# Start the server
echo "Starting server on $SERVER_IP:$SERVER_PORT..."
python manage makemigrations
python manage.py migrate
python manage.py runserver $SERVER_IP:$SERVER_PORT
