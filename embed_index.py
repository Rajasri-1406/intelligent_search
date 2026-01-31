import os
import sqlite3
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "papers.db")

conn = sqlite3.connect(DB_PATH)
rows = conn.execute("SELECT title, abstract FROM papers").fetchall()
conn.close()

print(f"Loaded {len(rows)} papers from DB")

if len(rows) == 0:
    raise ValueError("❌ No papers found in database. Run ingest.py first.")

texts = [f"{r[0]}. {r[1]}" for r in rows]

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True
)

print("Embedding shape:", embeddings.shape)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, os.path.join(BASE_DIR, "papers.index"))
pickle.dump(texts, open(os.path.join(BASE_DIR, "papers.pkl"), "wb"))

print("✅ Vector index built successfully")
