import os
import re

from dotenv import load_dotenv
import google.genai as genai

MODEL_NAME = "gemini-2.5-flash"


def load_document(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def chunk_document(doc: str) -> list[str]:
    chunks = [part.strip() for part in doc.split("\n\n") if part.strip()]
    return chunks


def score_overlap(question: str, chunk: str) -> int:
    q_words = set(re.findall(r"[a-zA-Z0-9']+", question.lower()))
    c_words = set(re.findall(r"[a-zA-Z0-9']+", chunk.lower()))
    return len(q_words & c_words)


def retrieve_chunks(question: str, chunks: list[str], top_k: int = 3) -> list[tuple[int, str]]:
    scored = [(i, chunk, score_overlap(question, chunk)) for i, chunk in enumerate(chunks)]
    scored.sort(key=lambda x: x[2], reverse=True)
    best = [(i, chunk) for i, chunk, score in scored if score > 0][:top_k]
    return best


def answer_from_context(client: genai.Client, question: str, selected: list[tuple[int, str]]) -> str:
    if not selected:
        return "I don't know. I could not find that in the document."

    context_blocks = []
    for idx, chunk in selected:
        context_blocks.append(f"[Chunk {idx + 1}]\n{chunk}")
    context = "\n\n".join(context_blocks)

    prompt = f"""
Answer the question using ONLY the provided context.
If the answer is not in the context, reply exactly: I don't know.
When possible, include the source chunk label like [Chunk 2].

Question:
{question}

Context:
{context}
""".strip()

    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return (response.text or "I don't know.").strip()


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Create .env from .env.example.")
        return

    file_path = input("Document path (default faq.txt): ").strip() or "faq.txt"
    try:
        doc = load_document(file_path)
    except FileNotFoundError:
        print(f"Error: file not found: {file_path}")
        return

    chunks = chunk_document(doc)
    client = genai.Client(api_key=api_key)

    print("FAQ Bot ready. Ask questions. Type /exit to quit.\n")
    while True:
        question = input("You: ").strip()
        if question == "/exit":
            print("Goodbye!")
            break
        if not question:
            continue

        selected = retrieve_chunks(question, chunks)
        answer = answer_from_context(client, question, selected)
        print(f"\nBot: {answer}\n")


if __name__ == "__main__":
    main()
