# Tells docker to Use a slim Python 3.12 base image (small, efficient, up-to-date)
FROM python:3.12-slim

# Set environment variable so Flask knows which file contains the app object
ENV FLASK_APP=main.py

# Set the working directory inside the container to /app
WORKDIR /app

# Copy only requirements first (better caching if code changes)
COPY requirements.txt .

# Install Python dependencies without caching (keeps image smaller)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into /app
COPY . .

# Document that this container serves on port 7774
EXPOSE 7774

# Start the Flask development server on all interfaces (0.0.0.0) and port 7774
CMD ["flask", "run", "--host=0.0.0.0", "--port=7774"]
