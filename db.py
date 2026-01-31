import sqlite3

conn = sqlite3.connect("papers.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS papers (
    id INTEGER PRIMARY KEY,
    title TEXT,
    abstract TEXT,
    authors TEXT,
    category TEXT
)
""")

conn.commit()
conn.close()
