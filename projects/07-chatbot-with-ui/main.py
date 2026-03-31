import os
import time
from datetime import datetime

from dotenv import load_dotenv
import google.genai as genai
import streamlit as st

DEFAULT_MODEL = "gemini-2.5-flash"
AVAILABLE_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash"]
QUICK_PROMPTS = [
    "Explain this topic in simple terms.",
    "Give me a step-by-step plan.",
    "Summarize this in 5 bullets.",
    "What are the risks and trade-offs?",
]


def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "started_at" not in st.session_state:
        st.session_state.started_at = datetime.now()
    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = ""


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, len(text) // 4)


def context_messages(messages: list[dict[str, str]], max_turns: int) -> list[dict[str, str]]:
    keep = max(1, max_turns) * 2
    return messages[-keep:]


def history_to_text(history: list[dict[str, str]]) -> str:
    lines = []
    for msg in history:
        role = "User" if msg["role"] == "user" else "Assistant"
        lines.append(f"{role}: {msg['content']}")
    return "\n".join(lines)


def chat_log_text(messages: list[dict[str, str]], model_name: str) -> str:
    header = [
        "AI Chat Log",
        f"Saved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Model: {model_name}",
        "",
        "=" * 50,
        "",
    ]
    body = []
    for msg in messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        body.append(f"{role}:\n{msg['content']}\n")
    return "\n".join(header + body)


def render_styles() -> None:
    st.markdown(
        """
        <style>
        .app-badge {
            display: inline-block;
            padding: 0.25rem 0.6rem;
            border-radius: 999px;
            background: #e8f1ff;
            color: #0a3d91;
            font-size: 0.82rem;
            font-weight: 600;
            border: 1px solid #bdd4ff;
            margin-bottom: 0.4rem;
        }
        .app-subtitle {
            color: #4b5563;
            margin-top: -0.2rem;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    st.set_page_config(page_title="AI Chat Studio", page_icon=":speech_balloon:", layout="wide")
    render_styles()
    init_state()

    st.markdown("<div class='app-badge'>Project 07</div>", unsafe_allow_html=True)
    st.title("AI Chat Studio")
    st.markdown("<p class='app-subtitle'>Modern Streamlit chat with Gemini, context controls, and export.</p>", unsafe_allow_html=True)

    if not api_key:
        st.error("GEMINI_API_KEY not found. Create .env from .env.example.")
        st.stop()

    with st.sidebar:
        st.header("Controls")
        model_name = st.selectbox("Model", AVAILABLE_MODELS, index=0)
        system_prompt = st.text_area(
            "System Prompt",
            value="You are a helpful assistant. Give concise and practical answers.",
            height=100,
        )
        max_turns = st.slider("Context Window (turns)", min_value=2, max_value=30, value=10)
        animate = st.toggle("Animate Responses", value=True)

        left, right = st.columns(2)
        if left.button("Clear", use_container_width=True):
            st.session_state.messages = []
            st.session_state.started_at = datetime.now()
            st.rerun()
        if right.button("Undo", use_container_width=True):
            if st.session_state.messages:
                st.session_state.messages.pop()
                if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                    st.session_state.messages.pop()
                st.rerun()

        if st.session_state.messages:
            st.download_button(
                "Download Chat Log",
                data=chat_log_text(st.session_state.messages, model_name),
                file_name=f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True,
            )

    client = genai.Client(api_key=api_key)

    total_chars = sum(len(m["content"]) for m in st.session_state.messages)
    total_tokens = estimate_tokens(total_chars * "x")
    c1, c2, c3 = st.columns(3)
    c1.metric("Messages", len(st.session_state.messages))
    c2.metric("Estimated Tokens", total_tokens)
    c3.metric("Session", st.session_state.started_at.strftime("%H:%M"))

    st.subheader("Quick Prompt")
    quick_cols = st.columns(len(QUICK_PROMPTS))
    for i, qp in enumerate(QUICK_PROMPTS):
        if quick_cols[i].button(qp, use_container_width=True):
            st.session_state.pending_prompt = qp

    st.divider()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type your message...")
    prompt = user_input or st.session_state.pending_prompt
    st.session_state.pending_prompt = ""
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    active_context = context_messages(st.session_state.messages, max_turns=max_turns)
    conversation = history_to_text(active_context)
    request_prompt = f"{system_prompt}\n\n{conversation}"

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.models.generate_content(model=model_name, contents=request_prompt)
            reply = (response.text or "Sorry, I could not generate a reply.").strip()

            if animate and reply:
                placeholder = st.empty()
                words = reply.split()
                rendered = []
                for word in words:
                    rendered.append(word)
                    placeholder.write(" ".join(rendered))
                    time.sleep(0.02)
            else:
                st.write(reply)
    except Exception as exc:
        reply = f"Error: failed to get response from Gemini. {exc}"
        with st.chat_message("assistant"):
            st.error(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
