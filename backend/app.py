# backend/app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd
import joblib
from langdetect import detect
import numpy as np
import os
import traceback
from fastapi.staticfiles import StaticFiles

MODEL_LOAD_ERROR = None

# ---------------------------------------------------
# 1. Initialize FastAPI app
# ---------------------------------------------------

app = FastAPI(title="Fake News Verifier (Multilingual Semantic Model)")

# ---------------------------------------------------
# 2. FIX: Allow frontend (index.html) to access backend
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow ALL websites (frontend)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, etc.
    allow_headers=["*"],  # Allow all headers
)

# ---------------------------------------------------
# 3. Load models one time when server starts
# ---------------------------------------------------

print("🔄 Loading models...")

try:
    import torch
    import gc

    torch.set_num_threads(1)

    model_source = (
        "models/embed_model"
        if os.path.exists("models/embed_model/model.safetensors")
        else "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    embed_model = SentenceTransformer(
        model_source,
        device="cpu",
        model_kwargs={"torch_dtype": torch.bfloat16, "low_cpu_mem_usage": True},
    )

    try:
        embed_model = torch.quantization.quantize_dynamic(
            embed_model, {torch.nn.Linear}, dtype=torch.qint8
        )
    except Exception as q_err:
        print("Note: Dynamic quantization skipped:", q_err)

    gc.collect()

    clf = joblib.load("models/clf_baseline.joblib")  # classifier
    training_data = pd.read_csv("data/train.csv")
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)
    training_features = tfidf_vectorizer.fit_transform(training_data["text"])
    tfidf_clf = LogisticRegression(max_iter=1000, random_state=42)
    tfidf_clf.fit(training_features, training_data["label"])

    del training_data, training_features
    gc.collect()

    print("✅ Semantic and TF-IDF models loaded successfully.")
except Exception as e:
    MODEL_LOAD_ERROR = str(e)
    print("❌ Error loading models:", e)

# ---------------------------------------------------
# 4. Input format
# ---------------------------------------------------


class InputText(BaseModel):
    text: str


# ---------------------------------------------------
# 5. Prediction endpoint
# ---------------------------------------------------


@app.post("/predict")
async def predict_text(data: InputText):
    try:
        if MODEL_LOAD_ERROR:
            return {"error": f"Model startup failed: {MODEL_LOAD_ERROR}"}

        text = data.text.strip()

        if text == "":
            return {"error": "No text provided"}

        # ---------------------------------------------------
        # Language detection (safe)
        # ---------------------------------------------------
        try:
            lang = detect(text)
        except:
            lang = "unknown"

        # ---------------------------------------------------
        # Embedding
        # ---------------------------------------------------
        emb = embed_model.encode([text])
        tfidf_features = tfidf_vectorizer.transform([text])

        # ---------------------------------------------------
        # Prediction
        # ---------------------------------------------------
        semantic_prob = clf.predict_proba(emb)[0]
        tfidf_prob = tfidf_clf.predict_proba(tfidf_features)[0]
        prob = (semantic_prob + tfidf_prob) / 2
        pred = int(np.argmax(prob))
        confidence = float(prob[pred])

        # ---------------------------------------------------
        # Output
        # ---------------------------------------------------
        return {
            "prediction": "FAKE" if pred == 1 else "REAL",
            "confidence": confidence,
            "language_detected": lang,
            "tfidf_confidence": float(tfidf_prob[pred]),
            "embedding_preview": emb[0][:8].tolist(),  # first 8 numbers for display
        }

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}


# ---------------------------------------------------
# 6. Serve UI directly at http://127.0.0.1:8001/
# ---------------------------------------------------
frontend_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")


# ---------------------------------------------------
# Run using:
# uvicorn backend.app:app --reload --host 127.0.0.1 --port 8001
# ---------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("backend.app:app", host="0.0.0.0", port=port)
