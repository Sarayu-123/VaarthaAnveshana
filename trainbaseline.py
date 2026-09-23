# train_baseline.py
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

print("Loading dataset...")
df = pd.read_csv("data/train.csv")

texts = df["text"].tolist()
labels = df["label"].tolist()

print("Loading embedding model...")
embed_model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

print("Creating embeddings...")
embeddings = embed_model.encode(texts, show_progress_bar=True)

print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    embeddings,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels,
)

print("Training classifier...")
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
print(f"Validation accuracy: {accuracy_score(y_test, predictions):.2%}")
print(classification_report(y_test, predictions, zero_division=0))

print("Saving models...")
embed_model.save("models/embed_model")
joblib.dump(clf, "models/clf_baseline.joblib")

print("Training completed successfully!")
