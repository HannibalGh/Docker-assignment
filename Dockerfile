# Use a slim Python 3.12 base image (lightweight, efficient, and up-to-date)
FROM python:3.12-slim

# Set environment variable so Flask knows which file contains the app instance
ENV FLASK_APP=main.py

# Set the working directory inside the container to /app
WORKDIR /app

# Copy only the requirements file first (improves build caching if code changes later)
COPY requirements.txt .

# Install Python dependencies without caching (keeps image size smaller)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . .

# Expose port 7774 so the app can be accessed from outside the container
EXPOSE 7774

# Run the Flask development server on all interfaces (0.0.0.0) at port 7774
CMD ["flask", "run", "--host=0.0.0.0", "--port=7774"]
