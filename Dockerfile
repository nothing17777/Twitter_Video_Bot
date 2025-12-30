# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
# ffmpeg is required for video processing
# nodejs is used by yt-dlp to handle some JS challenges on YouTube
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    unzip \
    && curl -fsSL https://deno.land/install.sh | sh \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add Deno to PATH
ENV PATH="/root/.deno/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create the /data directory for persistent storage
RUN mkdir -p /data

# Copy the rest of the application code
COPY . .

# Ensure usedVideo.txt exists so it can be used for tracking
RUN touch usedVideo.txt

# Command to run the scheduler
CMD ["python", "scheduler.py"]
