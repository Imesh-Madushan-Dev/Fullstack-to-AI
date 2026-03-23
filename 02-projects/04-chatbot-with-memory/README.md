# 04 — CLI Chatbot with Memory

**Level:** 🐇 Rabbit  
**Time:** 3–5 hours  
**Goal:** A terminal chatbot that remembers your full conversation — with a command to wipe it.

---

## What You're Building

An upgraded version of Project 01. This time, conversation history persists properly and you add user commands to control the session.

The key insight: the model itself has no memory. You are the memory. You store history and send it every time.

---

## What You'll Learn

- Proper conversation state management
- How context window limits affect long conversations
- How to implement slash commands in a CLI app

---

## Approach

1. Build on your Project 01 chatbot
2. Store messages in a list that persists for the whole session
3. Add a `/clear` command to reset history
4. Add a `/history` command to print the conversation so far
5. Handle edge case: what happens when conversation gets too long?

```python
# Core idea
messages = []
system_prompt = "You are a helpful assistant. Remember everything the user tells you."

def chat(user_input):
    messages.append({"role": "user", "content": user_input})
    response = client.messages.create(
        model="claude-opus-4-5",
        system=system_prompt,
        messages=messages,
        max_tokens=1024
    )
    reply = response.content[0].text
    messages.append({"role": "assistant", "content": reply})
    return reply
```

---

## Done When

- [ ] Chatbot remembers context across the whole session
- [ ] `/clear` resets the conversation
- [ ] `/history` prints everything said so far
- [ ] `/exit` closes cleanly

---

## Stretch Goals

- Add a system prompt that gives the bot a persona or specific role
- Warn the user when the context window is getting full
- Save history to a JSON file and reload it on next run
