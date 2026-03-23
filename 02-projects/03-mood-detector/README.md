# 03 — Mood Detector

**Level:** 🐜 Ant  
**Time:** 1–2 hours  
**Goal:** User types a sentence → AI classifies the mood and prints the result.

---

## What You're Building

A classifier. Give it any sentence and it returns a structured label — positive, negative, neutral, or something more specific like frustrated, excited, sad.

---

## What You'll Learn

- Structured outputs — getting the model to return predictable, parseable responses
- Classification prompting — forcing a specific answer format
- The difference between asking for freeform text vs. constrained output

---

## Approach

1. Take a sentence as input
2. Write a prompt that tells the model to respond ONLY with a label
3. Parse and display the result cleanly

```python
# Core idea
sentence = input("Enter a sentence: ")

prompt = f"""
Classify the mood of this sentence.
Respond with ONLY one of these labels: positive, negative, neutral, excited, frustrated, sad.
No other text.

Sentence: "{sentence}"
"""

response = client.messages.create(
    model="claude-opus-4-5",
    messages=[{"role": "user", "content": prompt}]
)

mood = response.content[0].text.strip()
print(f"Mood: {mood}")
```

---

## Done When

- [ ] Correctly classifies clearly positive and negative sentences
- [ ] Returns only the label — no extra explanation
- [ ] Handles weird or ambiguous input gracefully

---

## Stretch Goals

- Return a confidence score (1–10) alongside the label
- Detect mood from a whole paragraph, sentence by sentence
- Return JSON output: `{"mood": "positive", "confidence": 8}`
