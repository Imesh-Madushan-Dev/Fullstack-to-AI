import os

from dotenv import load_dotenv
import google.genai as genai
import streamlit as st

MODEL_NAME = "gemini-2.5-flash"


def history_to_text(history: list[dict[str, str]]) -> str:
    lines = []
    for msg in history:
        role = "User" if msg["role"] == "user" else "Assistant"
        lines.append(f"{role}: {msg['content']}")
    return "\n".join(lines)


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    st.set_page_config(page_title="Chatbot with UI", page_icon="💬")
    st.title("Chatbot with UI")
    st.caption("Project 07 - Streamlit + Gemini")

    if not api_key:
        st.error("GEMINI_API_KEY not found. Create .env from .env.example.")
        st.stop()

    client = genai.Client(api_key=api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Type a message...")
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    conversation = history_to_text(st.session_state.messages)
    request_prompt = (
        "You are a helpful assistant. Continue this conversation naturally.\n\n"
        f"{conversation}"
    )

    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=request_prompt)
        reply = (response.text or "Sorry, I could not generate a reply.").strip()
    except Exception:
        reply = "Error: failed to get response from Gemini."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)


if __name__ == "__main__":
    main()
