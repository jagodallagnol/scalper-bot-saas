FROM python:3.10-slim

# Install system dependencies needed to compile TA-Lib
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download, compile and install TA-Lib C library (required by python ta-lib)
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib*

# Set working directory for our app
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
# Install standard dependencies plus Gunicorn for robust web serving
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy all remaining bot source code
COPY . .

# Hugging Face Spaces uses port 7860
ENV PORT=7860
EXPOSE 7860

# Setup the command to run the backend API server 24/7
CMD ["gunicorn", "api_server:app", "--bind", "0.0.0.0:7860", "--workers", "1", "--threads", "4", "--timeout", "120"]
