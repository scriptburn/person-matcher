FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Pre-install Python build-time dependencies
RUN pip install --upgrade pip && pip install \
    numpy==1.24.4 \
    scipy \
    cython \
    wheel \
    pillow \
    opencv-python-headless \
    torch==2.0.1 \
    torchvision==0.15.2 \
    scikit-learn \
    streamlit \
    ultralytics

# Clone and install TorchReID (editable mode)
RUN git clone https://github.com/KaiyangZhou/deep-person-reid.git /torchreid
WORKDIR /torchreid
RUN pip install -r requirements.txt && python setup.py develop

# Return to app root (will be mounted in dev)
WORKDIR /app

EXPOSE 8501

CMD ["streamlit", "run", "web/app.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]