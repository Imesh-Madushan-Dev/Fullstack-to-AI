import os
from pathlib import Path

from dotenv import load_dotenv
import google.genai as genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = "gemini-2.5-flash"


def load_documents(folder: str) -> list[tuple[str, str]]:
    base = Path(folder)
    docs = []
    for path in sorted(base.glob("*.txt")) + sorted(base.glob("*.md")):
        docs.append((path.name, path.read_text(encoding="utf-8")))
    return docs


def chunk_text(text: str, chunk_size: int = 120, overlap: int = 30) -> list[str]:
    words = text.split()
    if not words:
        return []
    chunks = []
    step = max(1, chunk_size - overlap)
    for i in range(0, len(words), step):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks


def build_index(docs: list[tuple[str, str]]):
    entries = []
    for doc_name, content in docs:
        for idx, chunk in enumerate(chunk_text(content)):
            entries.append({"doc": doc_name, "chunk_id": idx + 1, "text": chunk})

    corpus = [e["text"] for e in entries]
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(corpus)
    return entries, vectorizer, matrix


def retrieve(question: str, entries, vectorizer, matrix, top_k: int = 5):
    q_vec = vectorizer.transform([question])
    scores = cosine_similarity(q_vec, matrix).flatten()
    ranked_idx = scores.argsort()[::-1][:top_k]
    results = []
    for idx in ranked_idx:
        if scores[idx] <= 0:
            continue
        e = entries[idx]
        results.append((float(scores[idx]), e))
    return results


def answer_question(client: genai.Client, question: str, retrieved) -> str:
    if not retrieved:
        return "I don't know. No relevant chunks were found."

    context_parts = []
    for score, e in retrieved:
        context_parts.append(
            f"[Source: {e['doc']} | chunk {e['chunk_id']} | score {score:.3f}]\n{e['text']}"
        )

    prompt = f"""
Answer the question using only the retrieved context.
If the answer is not present, say "I don't know.".
Include source tags from the context in your answer.

Question:
{question}

Retrieved context:
{"\n\n".join(context_parts)}
""".strip()

    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return (response.text or "I don't know.").strip()


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Create .env from .env.example.")
        return

    docs = load_documents("documents")
    if not docs:
        print("No documents found in ./documents")
        return

    entries, vectorizer, matrix = build_index(docs)
    print(f"Loaded {len(docs)} documents and indexed {len(entries)} chunks.")

    client = genai.Client(api_key=api_key)
    print("Ask questions. Type /exit to quit.\n")

    while True:
        question = input("You: ").strip()
        if question == "/exit":
            print("Goodbye!")
            break
        if not question:
            continue

        retrieved = retrieve(question, entries, vectorizer, matrix, top_k=5)
        answer = answer_question(client, question, retrieved)
        print(f"\nRAG: {answer}\n")


if __name__ == "__main__":
    main()
