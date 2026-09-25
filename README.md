# 📰 VaarthaAnveshana

### Multilingual Fake News Verification using NLP & Machine Learning

VaarthaAnveshana is a multilingual fake-news classification application that analyzes news text using **Sentence Transformer semantic embeddings** and **TF-IDF with Logistic Regression**.

The system combines semantic and lexical information from the input text to classify it as **REAL** or **FAKE**, while also detecting the language and providing prediction confidence.

---

## ✨ Features

* 🌐 **Multilingual Text Analysis**

  * Detects the language of the submitted text.
  * Uses a multilingual Sentence Transformer for semantic representation.

* 🧠 **Semantic Analysis**

  * Uses `paraphrase-multilingual-MiniLM-L12-v2` to generate semantic embeddings.

* 🔤 **TF-IDF Analysis**

  * Extracts unigram and bigram features from the input text.

* 🤖 **Machine Learning Classification**

  * Uses Logistic Regression for classification.

* 🔀 **Dual Prediction Approach**

  * Combines predictions from:

    * Semantic embedding-based classification
    * TF-IDF-based classification

* 📊 **Confidence Score**

  * Displays the probability associated with the predicted class.

* 🖥️ **Web Interface**

  * Interactive frontend for entering and analyzing news text.

* ⚡ **FastAPI Backend**

  * Provides a `/predict` API endpoint for classification.

* 🐳 **Docker Support**

  * Includes a Dockerfile for containerized execution.

---

## 🧠 How VaarthaAnveshana Works

The application processes the submitted text through two complementary NLP pipelines.

```text
                    NEWS TEXT
                        │
                        ▼
                Language Detection
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
     Sentence Transformer       TF-IDF
          Embeddings           Features
             │                     │
             ▼                     ▼
     Semantic Classifier      Logistic Regression
             │                     │
             └──────────┬──────────┘
                        │
                        ▼
              Probability Combination
                        │
                        ▼
                Final Prediction
                        │
                 ┌──────┴──────┐
                 ▼             ▼
               REAL           FAKE
```

### Step 1 — Language Detection

The submitted text is analyzed using `langdetect` to identify its language.

### Step 2 — Semantic Representation

The text is converted into semantic embeddings using:

`paraphrase-multilingual-MiniLM-L12-v2`

These embeddings capture the semantic meaning of the input text.

### Step 3 — Semantic Classification

The generated embeddings are passed to a trained classifier to obtain class probabilities.

### Step 4 — TF-IDF Representation

The same text is transformed using TF-IDF with:

* Unigrams
* Bigrams
* Sublinear TF scaling

### Step 5 — TF-IDF Classification

The TF-IDF representation is passed to a Logistic Regression classifier.

### Step 6 — Prediction Combination

The probability outputs from the semantic and TF-IDF classifiers are averaged.

The class with the highest combined probability becomes the final prediction.

---

## 🔬 Machine Learning Approach

### Semantic Model

```text
Model:
paraphrase-multilingual-MiniLM-L12-v2
```

The Sentence Transformer converts text into dense numerical embeddings that capture semantic relationships.

### TF-IDF Model

The application uses:

```text
TfidfVectorizer(
    ngram_range=(1, 2),
    sublinear_tf=True
)
```

This represents the input using both individual words and two-word combinations.

### Classifier

The TF-IDF features are classified using:

```text
Logistic Regression
```

The application therefore combines:

```text
Semantic Information
        +
Lexical Information
        ↓
Final Classification
```

---

## 📊 Prediction Output

The API returns information such as:

```json
{
  "prediction": "REAL",
  "confidence": 0.87,
  "language_detected": "en",
  "tfidf_confidence": 0.82,
  "embedding_preview": [
    0.021,
    -0.143,
    0.087
  ]
}
```

### Output Fields

| Field               | Description                                     |
| ------------------- | ----------------------------------------------- |
| `prediction`        | Final `REAL` or `FAKE` classification           |
| `confidence`        | Probability associated with the predicted class |
| `language_detected` | Detected language code                          |
| `tfidf_confidence`  | Probability from the TF-IDF classifier          |
| `embedding_preview` | Preview of the generated semantic embedding     |

---

## 🛠️ Tech Stack

### Programming Language

* Python

### Backend

* FastAPI
* Uvicorn
* Pydantic

### Natural Language Processing

* Sentence Transformers
* LangDetect
* TF-IDF

### Machine Learning

* Scikit-learn
* Logistic Regression
* Joblib

### Data Processing

* Pandas
* NumPy

### Frontend

* HTML
* CSS
* JavaScript

### Containerization

* Docker

---

## 📁 Project Structure

```text
VaarthaAnveshana/
│
├── backend/
│   └── app.py
│       └── FastAPI backend and prediction API
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
│       └── Web interface and API interaction
│
├── data/
│   └── train.csv
│       └── Training dataset
│
├── models/
│   ├── clf_baseline.joblib
│   │   └── Trained classifier
│   │
│   └── embed_model/
│       └── Saved Sentence Transformer model
│
├── docs/
│   └── SETUP_GUIDE.md
│       └── Setup documentation
│
├── Dockerfile
├── requirements.txt
├── trainbaseline.py
├── .gitignore
└── README.md
```

---

## 🚀 Running the Project Locally

### Prerequisites

Make sure the following are installed:

* Python 3.10+
* pip
* Git

### 1. Clone the Repository

```bash
git clone https://github.com/Sarayu-123/VaarthaAnveshana.git
```

### 2. Navigate to the Project

```bash
cd VaarthaAnveshana
```

### 3. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the FastAPI Server

```bash
uvicorn backend.app:app --reload --host 127.0.0.1 --port 7860
```

### 6. Open the Application

Open the following URL in your browser:

```text
http://127.0.0.1:7860/
```

---

## 🔌 API

### POST `/predict`

The `/predict` endpoint accepts news text and returns the classification result.

### Request

```json
{
  "text": "Your news statement here."
}
```

### Example using cURL

```bash
curl -X POST "http://127.0.0.1:7860/predict" \
     -H "Content-Type: application/json" \
     -d "{\"text\":\"Your news statement here.\"}"
```

---

## 🖥️ Application Architecture

```text
                        VaarthaAnveshana
                              │
                              ▼
                        Web Interface
                              │
                              │ POST /predict
                              ▼
                        FastAPI Backend
                              │
               ┌──────────────┴──────────────┐
               │                             │
               ▼                             ▼
       Language Detection             Text Processing
                                             │
                              ┌──────────────┴──────────────┐
                              │                             │
                              ▼                             ▼
                    Sentence Transformer              TF-IDF
                              │                             │
                              ▼                             ▼
                    Semantic Classifier          Logistic Regression
                              │                             │
                              └──────────────┬──────────────┘
                                             │
                                             ▼
                                   Probability Combination
                                             │
                                             ▼
                                      REAL / FAKE
```

---

## 🐳 Docker

The project includes a Dockerfile for containerized execution.

### Build the Docker Image

```bash
docker build -t vaarthaanveshana .
```

### Run the Container

```bash
docker run -p 7860:7860 vaarthaanveshana
```

Then open:

```text
http://localhost:7860/
```

---

## ⚠️ Limitations

VaarthaAnveshana is a **machine-learning-based classification system** and should not be considered an authoritative fact-checking service.

The prediction depends on factors such as:

* Quality and distribution of the training data
* Language of the input
* Domain of the news text
* Model generalization
* Characteristics of the submitted text

The confidence score represents the model's classification probability and should **not be interpreted as absolute certainty** that a claim is factually true or false.

The current system classifies the supplied text and does not independently verify the claim against external authoritative sources.

---

## 🔮 Future Enhancements

* 🔎 Evidence retrieval from trusted sources
* 📰 Integration with fact-checking databases
* 🌐 Improved multilingual datasets
* 📚 Source credibility analysis
* 🧩 Claim-level verification
* 💡 Explainable predictions
* 📊 Model evaluation and analytics dashboard
* 🔄 Continuous model improvement
* 🧠 Retrieval-Augmented Generation for evidence-based verification
* 🔗 Integration with trusted news and fact-checking APIs

---

## 🎯 Project Highlights

VaarthaAnveshana brings together multiple areas of AI and software development:

```text
Natural Language Processing
          +
Semantic Embeddings
          +
TF-IDF
          +
Machine Learning
          +
FastAPI
          +
Frontend Development
          +
Docker
```

The project demonstrates the integration of an NLP/ML pipeline into a complete web application rather than using the model only as an isolated experiment.

---

## 📌 Project Status

**Status:** Active Development

The current version focuses on multilingual fake-news classification using semantic embeddings and TF-IDF-based machine learning.

---

## 👩‍💻 Author

### N. Ch. Krishna Sri Sarayu

B.Tech — Computer Science Engineering
Specialization — Artificial Intelligence & Machine Learning

**GitHub:**
[https://github.com/Sarayu-123](https://github.com/Sarayu-123)

---

## ⭐ Support

If you find VaarthaAnveshana interesting, consider giving the repository a ⭐ on GitHub.

---

<p align="center">

### 📰 VaarthaAnveshana

**Vaartha · Anveshana · Intelligence through Language**

</p>
