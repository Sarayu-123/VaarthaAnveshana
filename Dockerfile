FROM python:3.10-slim

# Set up user with UID 1000 for Hugging Face Spaces security requirements
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin: \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements and install dependencies
COPY --chown=user requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files (model.safetensors excluded via .dockerignore)
COPY --chown=user . /app

# Pre-download the SentenceTransformer model from HuggingFace at build time
# so it's baked into the image and doesn't need internet on startup
RUN python -c "\
from sentence_transformers import SentenceTransformer; \
import os; \
os.makedirs('models/embed_model', exist_ok=True); \
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'); \
model.save('models/embed_model'); \
print('Model saved to models/embed_model')"

# Expose Railway / Hugging Face Space default port
EXPOSE 7860

# Start FastAPI application
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "7860"]
