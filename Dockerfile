FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements
COPY requirements.txt /app/requirements.txt

# Install CPU-only PyTorch first (reduces image from >4GB to ~300MB, preventing OOM / disk crashes on Railway)
# Then install remaining packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app

# Setup non-root user
RUN useradd -m -u 1000 user && \
    chown -R user:user /app /home/user

USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

EXPOSE 7860

# Start server using dynamic Railway PORT (defaults to 7860)
CMD ["sh", "-c", "uvicorn backend.app:app --host 0.0.0.0 --port ${PORT:-7860}"]
