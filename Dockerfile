FROM python:3.10-slim

# Install system dependencies including python3-dev for Python header files
# python3-dev is critical for compiling C extensions like ta-lib in slim images
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Download, compile and install TA-Lib C library
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib*

# Set working directory
WORKDIR /app

# Upgrade build tools globally first
RUN pip install --no-cache-dir --upgrade pip setuptools wheel numpy

# Expose TA-Lib paths to pip manually
ENV TA_LIBRARY_PATH=/usr/lib
ENV TA_INCLUDE_PATH=/usr/include

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy all remaining bot source code
COPY . .

# Hugging Face Spaces uses port 7860
ENV PORT=7860
EXPOSE 7860

# Setup the command to run the backend API server 24/7
CMD ["gunicorn", "api_server:app", "--bind", "0.0.0.0:7860", "--workers", "1", "--threads", "4", "--timeout", "120"]
