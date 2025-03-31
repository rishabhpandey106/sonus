# Use official Python 3.11.11 as the base image
FROM python:3.11.11

# Set working directory
WORKDIR /app

# Install ffmpeg and other minimal dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip (optional) and install only necessary Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install streamlit

# Copy application files
COPY audio/ /app/audio/
COPY video/ /app/video/
COPY transcript/ /app/transcript/
COPY extract_audio.py /app/extract_audio.py
COPY generate_srt.py /app/generate_srt.py
COPY transcript.py /app/transcript.py

# Expose port 8501 for Streamlit
EXPOSE 8501

# Run the application with Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
