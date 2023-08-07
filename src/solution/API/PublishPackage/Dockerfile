# Use the official Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the app's dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app's source code to the container
COPY . .

# Expose port 8000
EXPOSE 8000

# Start the Flask app when the container runs
CMD ["python", "app.py"]
