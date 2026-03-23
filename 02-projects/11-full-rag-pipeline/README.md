# 11 — Full RAG Pipeline

**Level:** 🐺 Wolf  
**Time:** 10–16 hours  
**Goal:** Ingest 50+ documents, store them properly, and answer questions accurately at scale.

---

## What You're Building

A production-grade RAG system. Not the hacky "paste the whole doc" approach from Project 05 — this uses real embeddings and a vector database to retrieve only what's relevant.

---

## What You'll Learn

- Embeddings — converting text into vectors that capture semantic meaning
- Vector databases — storing and searching embeddings efficiently
- Retrieval quality — the difference between keyword search and semantic search
- Chunking strategies — how you split documents matters a lot

---

## Approach

1. Collect 50+ documents (or a large text corpus)
2. Chunk each document into ~400 token pieces with overlap
3. Generate embeddings for each chunk (using OpenAI or HuggingFace)
4. Store embeddings in a vector DB (Pinecone, Weaviate, or pgvector)
5. At query time: embed the question → find top 5 similar chunks → send to model

```python
# Generate embedding for a chunk
from openai import OpenAI
client = OpenAI()

def embed(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Store in vector DB, then search at query time
# top_chunks = vector_db.search(embed(question), top_k=5)
```

---

## Tech Stack Options

| Component | Simple | Production |
|-----------|--------|------------|
| Embeddings | OpenAI `text-embedding-3-small` | HuggingFace (free, local) |
| Vector DB | ChromaDB (local, free) | Pinecone (hosted) |
| Orchestration | Raw Python | LangChain / LlamaIndex |

---

## Done When

- [ ] 50+ documents ingested and searchable
- [ ] Answers are accurate and sourced from the right documents
- [ ] Works better than the naive "paste everything" approach from Project 05

---

## Stretch Goals

- Evaluate retrieval quality — are you finding the right chunks?
- Try different chunk sizes and compare accuracy
- Add metadata filtering — search only within a specific doc or date range
