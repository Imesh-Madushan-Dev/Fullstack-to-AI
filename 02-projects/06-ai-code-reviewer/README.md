# 06 — AI Code Reviewer

**Level:** 🐇 Rabbit  
**Time:** 3–5 hours  
**Goal:** Paste your code → get a structured review with specific suggestions.

---

## What You're Building

A code review tool you'll actually use. Paste any function or file and get back a structured critique — bugs, improvements, readability notes.

---

## What You'll Learn

- Domain-specific system prompts — how to make the model an expert
- Structured output formatting — making the response consistent every time
- How to use AI as a personal code reviewer on real projects

---

## Approach

1. Write a system prompt that makes the model a senior code reviewer
2. Accept code as input (paste in terminal or read from file)
3. Define the output format in your prompt — make it consistent
4. Print the review cleanly

```python
# Core idea
system_prompt = """
You are a senior software engineer doing a code review.
For every piece of code, provide:
1. BUGS: Any errors or potential issues
2. IMPROVEMENTS: Specific suggestions with examples
3. READABILITY: Comments on clarity and style
4. SCORE: A rating from 1-10

Be specific. Reference line numbers when possible.
"""

code = open("my_function.py").read()
# Send to API with system prompt above
```

---

## Done When

- [ ] Reviews real code from your own projects
- [ ] Output is structured consistently every time
- [ ] Catches at least one real bug or improvement in your code

---

## Stretch Goals

- Add language detection — different review style for Python vs JS
- Add a `--strict` flag for harsh reviews and `--friendly` for gentle ones
- Build a simple before/after diff view
