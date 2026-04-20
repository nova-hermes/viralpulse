FROM python:3.11-slim

WORKDIR /app

# Install system deps (ffmpeg only)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install ONLY web dependencies (skip whisper/google bloat)
COPY requirements-web.txt ./
RUN pip install --no-cache-dir -r requirements-web.txt \
    Pillow>=10.0.0 \
    edge-tts>=6.1.0 \
    PyYAML>=6.0 \
    feedparser>=6.0.0 \
    requests>=2.31.0

# Copy application
COPY . .

# Create data dirs
RUN mkdir -p data/drafts data/media

# Expose port
EXPOSE 8080

# Run the web server (use Railway's PORT env var if available)
CMD uvicorn web.app:app --host 0.0.0.0 --port ${PORT:-8080}
