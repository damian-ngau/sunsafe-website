# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for the OpenWeatherMap API key
ENV OPENWEATHER_API_KEY=b084de8ed662689608025d696c949e17

# Run the app.py when the container launches
CMD ["python", "app.py"]
