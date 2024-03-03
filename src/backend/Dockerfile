# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

ARG PYTHON_VERSION=3.11.7
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /backend

# Copy requirements
COPY pyproject.toml poetry.lock .

# Install dependencies
RUN pip install poetry && poetry install

# Copy the local directory
COPY . .

# Copy the database file into the container
COPY weather.db /backend

# Expose the port that the application listens on.
EXPOSE 5000

# Run database migrations with Alembic
CMD poetry run alembic upgrade head

# Run the application.
CMD poetry run uvicorn 'main:app' --reload --host=0.0.0.0 --port=5000
