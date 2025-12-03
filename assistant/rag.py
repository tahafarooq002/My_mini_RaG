import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# -------------------------------
# CONFIG
# -------------------------------
HF_TOKEN = "Your_HF_Token"  # <-- Replace with your HF token
MODEL_NAME = "Your_LLM_Model"# <-- Replace with your LLM Model

# Initialize OpenAI-compatible client (Hugging Face)`
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN
)

# FAISS index and metadata paths
INDEX_PATH = "index/faiss.index"
META_PATH = "index/meta.json"

# Embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------------
# LOAD FAISS + METADATA
# -------------------------------
if not Path(INDEX_PATH).exists():
    raise FileNotFoundError("❌ FAISS index not found. Build index first.")

if not Path(META_PATH).exists():
    raise FileNotFoundError("❌ meta.json not found. Build index first.")

index = faiss.read_index(INDEX_PATH)

with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)

# -------------------------------
# HANDLE BOTH LIST & DICT META.JSON
# -------------------------------
if isinstance(meta, list):
    # Format: [{"doc_id": "...", "text": "..."}, ...]
    documents = [item["text"] for item in meta]
    doc_ids = [item["doc_id"] for item in meta]
elif isinstance(meta, dict):
    # Format: {"documents": [...], "doc_ids": [...]}
    documents = meta.get("documents", [])
    doc_ids = meta.get("doc_ids", [])
else:
    raise ValueError("❌ meta.json format not recognized")

# -------------------------------
# EMBED TEXT
# -------------------------------
def embed(text):
    return embed_model.encode([text])[0].astype("float32")

# -------------------------------
# RETRIEVE TOP-K
# -------------------------------
def retrieve(query, k=5):
    q_vec = embed(query)
    D, I = index.search(np.array([q_vec]), k)

    results = []
    for idx in I[0]:
        if idx != -1:
            results.append({
                "doc_id": doc_ids[idx],
                "text": documents[idx]
            })

    return results

# -------------------------------
# BUILD PROMPT
# -------------------------------
def build_prompt(question, docs):
    context_chunks = "\n\n".join(
        [f"[Source {d['doc_id']}]\n{d['text']}" for d in docs]
    )

    prompt = f"""
You are an AI assistant using a RAG system.

Use ONLY the following retrieved documents to answer the question.
If the answer is not present, reply with:
"I don't have enough information from the documents."

---------------------
Retrieved Documents:
---------------------
{context_chunks}

---------------------
Question:
---------------------
{question}

Final Answer:
"""
    return prompt

# -------------------------------
# MAIN RAG FUNCTION USING HUGGING FACE
# -------------------------------
def answer_query(question):
    docs = retrieve(question)
    if not docs:
        return "❌ No relevant documents found.", []

    prompt = build_prompt(question, docs)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
        )
        output = response.choices[0].message.content
    except Exception as e:
        return f"❌ HF API Error: {e}", docs

    return output, docs

# -------------------------------
# TEST
# -------------------------------
if __name__ == "__main__":
    query = "Who is Elizabeth Bennet?"
    answer, sources = answer_query(query)

    print("\nANSWER:", answer)
    print("\nSOURCES:", [s["doc_id"] for s in sources])
