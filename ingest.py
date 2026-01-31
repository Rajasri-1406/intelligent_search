import os
import json
import sqlite3
import ast  # for converting stringified lists to Python objects

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "papers.db")
JSON_PATH = os.path.join(BASE_DIR, "..", "data", "arxivData.json")

# Recreate DB
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS papers")
cur.execute("""
CREATE TABLE papers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    abstract TEXT,
    authors TEXT,
    category TEXT
)
""")

LIMIT = 24000
count = 0

print("Loading JSON file... this may take a minute")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, dict) and "papers" in data:
    data = data["papers"]

print(f"Total papers in JSON: {len(data)}")
if len(data) > 0:
    print("First paper sample:", data[0])

for paper in data:
    # Title
    title = str(paper.get("title", "")).replace("\n", " ").strip()

    # Abstract (from summary)
    abstract = str(paper.get("summary", "")).replace("\n", " ").strip()

    # Authors: stringified list
    authors_str = paper.get("author", "[]")
    try:
        authors_list = ast.literal_eval(authors_str)  # convert string -> list of dicts
        authors = ", ".join([a.get("name", "").strip() for a in authors_list])
    except:
        authors = authors_str  # fallback

    # Categories: stringified list
    tag_str = paper.get("tag", "[]")
    try:
        tag_list = ast.literal_eval(tag_str)
        category = ", ".join([t.get("term", "").strip() for t in tag_list])
    except:
        category = tag_str  # fallback

    # Insert if title and abstract exist
    if title and abstract:
        cur.execute(
            "INSERT INTO papers (title, abstract, authors, category) VALUES (?, ?, ?, ?)",
            (title, abstract, authors, category)
        )
        count += 1

    if count >= LIMIT:
        break

conn.commit()
conn.close()
print(f"✅ Successfully indexed {count} papers from arxivData.json")
