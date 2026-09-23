---
title: Fake News Verifier
emoji: 📰
colorFrom: yellow
colorTo: amber
sdk: docker
app_port: 7860
pinned: false
---

# Fake News Verifier

A multilingual fake news verification tool powered by semantic embeddings (SentenceTransformer) and TF-IDF logistic regression.

## Project Structure

`
├── backend/
│   └── app.py              # FastAPI server & prediction endpoint
├── frontend/
│   ├── index.html          # Web UI interface
│   ├── styles.css          # Newspaper & vintage style theme
│   └── app.js              # Frontend interactions & API calls
├── data/
│   └── train.csv           # Training dataset
├── models/
│   ├── clf_baseline.joblib # Trained baseline classifier
│   └── embed_model/        # Saved SentenceTransformer model
├── docs/
│   └── SETUP_GUIDE.md      # Environment setup instructions
├── Dockerfile              # Container deployment for Hugging Face Spaces
├── requirements.txt        # Python dependencies
└── trainbaseline.py        # Model training script
`

## Setup & Running Locally

1. **Install dependencies**:
   `ash
   pip install -r requirements.txt
   `

2. **Start the server**:
   `ash
   uvicorn backend.app:app --reload --host 127.0.0.1 --port 7860
   `

3. **Access the application**:
   Open http://127.0.0.1:7860/ in your browser.
