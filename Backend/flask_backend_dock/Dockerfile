# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /flask_backend_dock

# Copy the current directory contents into the container at /app
COPY . /flask_backend_dock

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 3000

# Run app.py when the container launches
CMD ["python", "app.py"]