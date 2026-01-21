FROM python:3.9-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY ./backend/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Download NLP models (doing this after pip install to ensure libraries exist)
RUN python -m spacy download en_core_web_sm
RUN python -m nltk.downloader stopwords punkt

# Copy the rest of the application
COPY ./backend/app /app/app
COPY ./frontend /app/frontend

# Create uploads directory
RUN mkdir -p /app/uploads

# Expose port
EXPOSE 8000

# Command to run the application
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"
