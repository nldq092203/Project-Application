#!/bin/bash
set -e

# Install pipenv if it's not installed
pip install pipenv

# Install dependencies from Pipfile.lock
pipenv install --deploy --ignore-pipfile

# Run database migrations
pipenv run python manage.py migrate

# Collect static files
pipenv run python manage.py collectstatic --noinput