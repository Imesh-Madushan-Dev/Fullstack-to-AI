# 08 — Document Q&A App

**Level:** 🦊 Fox  
**Time:** 6–10 hours  
**Goal:** Upload a PDF → ask questions about it → get accurate answers.

---

## What You're Building

A smarter version of Project 05. This time you handle real file uploads, extract text from PDFs, and build a proper UI around it. Think: ChatPDF, but built by you.

---

## What You'll Learn

- File upload handling in a web app
- PDF text extraction
- Embeddings — turning text into numbers that represent meaning
- Vector search — finding the most relevant chunks for a given question

---

## Approach

1. Accept a PDF upload in the UI
2. Extract text using `pypdf` or `pdfplumber`
3. Chunk the text into ~500 word pieces
4. For each question, find the most relevant chunk (keyword match for simple, embeddings for advanced)
5. Send the question + relevant chunk to the API

```python
# Extract text from PDF
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    text = "\n".join(page.extract_text() for page in pdf.pages)

# Chunk it
def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
```

---

## Done When

- [ ] Upload a PDF and ask questions about it
- [ ] Answers come from the document, not the model's general knowledge
- [ ] Works with a 10+ page document

---

## Stretch Goals

- Use real embeddings (OpenAI or Hugging Face) for smarter chunk retrieval
- Support multiple file uploads at once
- Show which page the answer came from
