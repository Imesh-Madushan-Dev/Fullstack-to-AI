# 07 — Chatbot with a UI

**Level:** 🦊 Fox  
**Time:** 4–8 hours  
**Goal:** Take your terminal chatbot and wrap it in a real web interface.

---

## What You're Building

A browser-based chatbot. Same logic as Project 04, but now with a UI that anyone can use — not just you in a terminal.

---

## What You'll Learn

- Connecting an AI backend to a frontend (your existing strength)
- Streaming responses — displaying text as it generates, not after
- Session state management in a web context

---

## Approach

**Option A — Quick (Streamlit):**  
Streamlit lets you build a UI in pure Python. Great for getting something up fast.

```python
import streamlit as st

st.title("My AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Type a message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Call API and append response
```

**Option B — Use Your Full-Stack Skills:**  
Build a FastAPI backend + React/Next.js frontend. More work, but you'll learn more and it'll be more impressive.

---

## Done When

- [ ] Chat UI renders in the browser
- [ ] Conversation history shows on screen
- [ ] Works for multiple back-and-forth messages

---

## Stretch Goals

- Add streaming so text appears word by word (not all at once)
- Add a "Clear Chat" button
- Deploy it — Vercel, Railway, or Render (free tiers available)
