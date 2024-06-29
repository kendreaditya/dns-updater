# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir requests python-dotenv

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run update_dns.py when the container launches
CMD ["python", "src/update_dns.py"]

# Run test_update_dns.py which tests if the dns is corretly updateing
# CMD ["python", "src/test_update_dns.py"]