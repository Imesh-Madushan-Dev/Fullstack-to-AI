# 01 — AI Chat in Terminal

**Level:** 🐜 Ant  
**Time:** 2–4 hours  
**Goal:** Have a back-and-forth conversation with an AI in your terminal.

---

## What You're Building

A simple command-line chatbot. You type, it responds. That's it.  
No UI, no framework. Just raw Python talking to an API.

---

## What You'll Learn

- How to make API calls to Claude / OpenAI
- How message history works (the model has no memory — you send the full conversation every time)
- What tokens and context windows feel like in practice

---

## Approach

1. Install the Anthropic Python SDK — `pip install anthropic`
2. Write a loop that takes user input
3. Append each message to a history list
4. Send the full history to the API each time
5. Print the response and loop again

```python
# Core idea
messages = []

while True:
    user_input = input("You: ")
    messages.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-opus-4-5",
        messages=messages
    )

    reply = response.content[0].text
    messages.append({"role": "assistant", "content": reply})
    print(f"AI: {reply}\n")
```

---

## Done When

- [ ] Multi-turn conversation works in the terminal
- [ ] The AI remembers what you said earlier in the session
- [ ] Typing "exit" ends the chat cleanly

---

## Stretch Goals

- Add a token counter to see how much context you're using
- Add a `/clear` command to reset the conversation
- Save the chat log to a `.txt` file on exit
