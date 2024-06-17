FROM python:3.10.4-alpine

WORKDIR /usr/src/app

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# Ensure Python output is sent straight to terminal
ENV PYTHONUNBUFFERED 1