import os
import re

from dotenv import load_dotenv
import google.genai as genai
from pypdf import PdfReader
import streamlit as st

MODEL_NAME = "gemini-2.5-flash"


def extract_text(uploaded_file) -> str:
    name = uploaded_file.name.lower()
    if name.endswith(".txt"):
        return uploaded_file.getvalue().decode("utf-8", errors="ignore")
    if name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return "\n".join(pages)
    return ""


def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    words = text.split()
    if not words:
        return []
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i : i + chunk_size]))
    return chunks


def overlap_score(question: str, chunk: str) -> int:
    q = set(re.findall(r"[a-zA-Z0-9']+", question.lower()))
    c = set(re.findall(r"[a-zA-Z0-9']+", chunk.lower()))
    return len(q & c)


def top_chunks(question: str, chunks: list[str], k: int = 3) -> list[tuple[int, str]]:
    scored = [(idx, chunk, overlap_score(question, chunk)) for idx, chunk in enumerate(chunks)]
    scored.sort(key=lambda x: x[2], reverse=True)
    return [(idx, chunk) for idx, chunk, score in scored if score > 0][:k]


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    st.set_page_config(page_title="Document Q&A", page_icon="📄")
    st.title("Document Q&A App")
    st.caption("Upload PDF/TXT and ask questions")

    if not api_key:
        st.error("GEMINI_API_KEY not found. Create .env from .env.example.")
        st.stop()

    uploaded = st.file_uploader("Upload a .pdf or .txt document", type=["pdf", "txt"])
    if not uploaded:
        st.info("Upload a file to start.")
        return

    text = extract_text(uploaded)
    if not text.strip():
        st.error("Could not extract text from this file.")
        return

    chunks = chunk_text(text, chunk_size=500)
    st.success(f"Document loaded. Created {len(chunks)} chunks.")

    question = st.text_input("Ask a question about the document")
    if not question.strip():
        return

    selected = top_chunks(question, chunks, k=3)
    if not selected:
        st.warning("No relevant context found in the document.")
        return

    context = "\n\n".join([f"[Chunk {i + 1}]\n{chunk}" for i, chunk in selected])
    prompt = f"""
Answer using ONLY the context below. If the answer is missing, say: I don't know.

Question:
{question}

Context:
{context}
""".strip()

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        answer = (response.text or "I don't know.").strip()
    except Exception:
        st.error("Failed to get response from Gemini.")
        return

    st.subheader("Answer")
    st.write(answer)

    with st.expander("Show source chunks"):
        for i, chunk in selected:
            st.markdown(f"**Chunk {i + 1}**")
            st.write(chunk)


if __name__ == "__main__":
    main()
