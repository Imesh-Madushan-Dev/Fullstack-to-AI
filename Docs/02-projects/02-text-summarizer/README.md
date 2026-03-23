# 02 — AI Text Summarizer

**Level:** 🐜 Ant  
**Time:** 1–2 hours  
**Goal:** Paste a long article, get a clean 3-line summary back.

---

## What You're Building

A script that takes any long text as input and returns a short, readable summary.  
Simple input → simple output. No loops, no history needed.

---

## What You'll Learn

- Prompt engineering basics — how you word the prompt changes the output drastically
- How to control output format (bullet points, paragraph, length)
- Handling user input from the terminal or a file

---

## Approach

1. Accept input — either paste text directly or read from a `.txt` file
2. Write a clear prompt that tells the model exactly what format you want
3. Send it to the API and print the result

```python
# Core idea
text = open("article.txt").read()

prompt = f"""
Summarize the following text in exactly 3 bullet points.
Each bullet should be one sentence. Be concise.

TEXT:
{text}
"""

response = client.messages.create(
    model="claude-opus-4-5",
    messages=[{"role": "user", "content": prompt}]
)

print(response.content[0].text)
```

---

## Done When

- [ ] Paste any article and get a 3-point summary
- [ ] Try different prompt wordings and notice how output changes
- [ ] Can read from both a file and direct text input

---

## Stretch Goals

- Let the user choose summary length (short / medium / detailed)
- Add a `--bullets` or `--paragraph` flag to control format
- Try summarizing in a different language
