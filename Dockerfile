FROM python:3.11-slim

WORKDIR /app

# Install system deps for ffmpeg and whisper
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt requirements-web.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-web.txt

# Copy application
COPY . .

# Create data dirs
RUN mkdir -p data/drafts data/media

# Expose port
EXPOSE 8080

# Run the web server
CMD ["uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8080"]
