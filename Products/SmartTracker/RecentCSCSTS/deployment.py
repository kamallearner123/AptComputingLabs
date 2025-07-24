import os
from .settings import *
from .settings import BASE_DIR

# Allow all hosts: WEBSITE_HOSTNAME is set in Azure App Service
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]

# CSRF_TRUSTED_ORIGINS is required for Azure App Service to allow CSRF protection
# CSRF stands for Cross-Site Request Forgery, a security vulnerability that allows 
# an attacker to trick a user into submitting a request that they did not intend to make.
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]

# DEBUG disabled for production. Because this is a production environment, 
# it is important to disable DEBUG mode to prevent sensitive information from being exposed. Like below:
# Using the URLconf defined in RecentCSCSTS.urls, Django tried these URL patterns, in this order:
# admin/
# accounts/ [name='home_page']
# accounts/ home/ [name='home']
# accounts/ signup/ [name='signup']
# accounts/ register/ [name='signup']
DEBUG = False

# whitenoise.middleware.WhiteNoiseMiddleware : This middleware is used for serving static files in production.
# why these middlewares are used:
# 1. SecurityMiddleware: Provides security enhancements.
# When a client requests the homepage in a Django application using whitenoise, 
# the static files (e.g., CSS, JavaScript, images) are not copied to the client on every request. 
# Instead, whitenoise serves the static files from the STATIC_ROOT directory (e.g., staticfiles), 
# where they were previously collected by running python manage.py collectstatic. 
# These files are sent to the client’s browser only when referenced in the 
# HTML (e.g., via <link> or <script> tags), and whitenoise optimizes delivery with compression and caching. 
# Subsequent requests may use cached files in the browser, reducing server load.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
]

#whitenoise.storage.CompressedManifestStaticFilesStorage ?

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Why is this connection string used?
# The connection string is used to connect to the Azure PostgreSQL database.
# It contains the necessary parameters such as database name, user, password, host, and port.
# This allows the Django application to interact with the database for data storage and retrieval.
# The connection string is typically set as an environment variable in Azure App Service for security reasons.
# The connection string is expected to be in the format:
# "dbname=your_db_name user=your_user password=your_password host=your_host port=your_port"
connection_string = os.environ.get('AZURE_POSTGRESSQL_CONNECTIONSTRING', None)
parameters = {param.split('=')[0]: param.split('=')[1] for param in connection_string.split(" ")}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': parameters['dbname'],
        'USER': parameters['user'],
        'PASSWORD': parameters['password'],
        'HOST': parameters['host'],
        'PORT': parameters['port'],
    }
}

