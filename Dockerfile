# Use the official Python image
FROM python:3.11.3

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies (if you have a requirements.txt file)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Flask will use
EXPOSE 8080

# Command to run the Flask application
CMD ["python", "main.py"]
