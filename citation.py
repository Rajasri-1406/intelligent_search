import re

def extract_citations(texts):
    citations = []
    for t in texts:
        found = re.findall(r"\b(19|20)\d{2}\b", t)
        citations.extend(found)
    return len(set(citations))
