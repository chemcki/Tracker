# Pull base image
FROM python:3.13-slim-bullseye

# Set environment variables
# Avoids pip warnings by disabling an automatic check for pip updates each time
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

# Set work directory (will be same directory in docker-compose.yml volumes)
WORKDIR /practice


COPY ./requirements.txt .
# For development can use RUN pip install --no-cache-dir -r requirements.txt for smaller image
RUN pip install -r requirements.txt

# Copy project
COPY . .