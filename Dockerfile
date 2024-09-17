# Use a more robust Python runtime as a base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python packages individually with --no-deps
RUN pip install --no-cache-dir --no-deps fastapi==0.114.2 && \
    pip install --no-cache-dir --no-deps uvicorn==0.24.0 && \
    pip install --no-cache-dir --no-deps sqlalchemy==2.0.25

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
