# 05 — AI FAQ Bot

**Level:** 🐇 Rabbit  
**Time:** 4–6 hours  
**Goal:** Feed it a document → ask questions → get accurate answers from that document only.

---

## What You're Building

Your first taste of RAG (Retrieval-Augmented Generation). You give the bot a source document, and it answers questions based only on that content — not from its general training.

---

## What You'll Learn

- How to inject custom context into a prompt
- The basics of RAG — why you can't just paste a 100-page doc into every prompt
- Chunking — breaking a document into smaller pieces
- Grounding responses in a source (reducing hallucinations)

---

## Approach

1. Read a text file (your resume, a product FAQ, documentation, anything)
2. For simple version: paste the whole file into the system prompt
3. Ask questions — the bot answers only from that content
4. For advanced version: chunk the doc and only send the relevant chunk

```python
# Simple approach (works for short docs)
doc = open("faq.txt").read()

system_prompt = f"""
You are a helpful assistant. Answer questions ONLY based on the document below.
If the answer is not in the document, say "I don't know."

DOCUMENT:
{doc}
"""

# Then run it like your Project 04 chatbot
```

---

## Done When

- [ ] Bot answers questions from your chosen document
- [ ] Bot says "I don't know" for things not in the document (doesn't hallucinate)
- [ ] Works with at least a 2–3 page document

---

## Stretch Goals

- Try it on a long document — what breaks? Where does context run out?
- Chunk the document into paragraphs and only send the most relevant chunk
- Add a source citation — "Based on paragraph 3..."
