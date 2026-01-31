from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search import semantic_search
from llm import generate_answer
from citation import extract_citations

app = FastAPI()

# 🔥 ADD THIS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search(query: str):
    docs = semantic_search(query)
    answer = generate_answer(query, docs)
    citations = extract_citations(docs)

    return {
        "query": query,
        "papers_used": len(docs),
        "citations": citations,
        "answer": answer
    }
