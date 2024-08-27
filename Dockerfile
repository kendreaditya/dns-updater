# Dockerfile

# Base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Install cron and dependencies
RUN apt-get update && \
    apt-get -y install cron && \
    pip install --no-cache-dir -r requirements.txt

# Give execution rights to the cron job
RUN chmod 0644 src/cronjob

# Apply cron job
RUN crontab src/cronjob

# Run cron in the foreground
CMD ["cron", "-f"]
