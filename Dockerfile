# Use an official Python runtime as the base image
FROM python:3.8

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the container
COPY . .

# Set the environment variable for Flask and the exposed port
ENV FLASK_APP=main.py
ENV PORT_DETECTION=5000

# Expose the specified port
EXPOSE $PORT_DETECTION

# Run the Flask application
CMD [ "sh", "-c", "flask run --host 0.0.0.0 --port ${PORT_DETECTION}"]
