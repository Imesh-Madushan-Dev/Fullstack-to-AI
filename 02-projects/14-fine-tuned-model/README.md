# 14 — Fine-Tuned Model

**Level:** 🐘 Elephant  
**Time:** 20–40 hours  
**Goal:** Take an open-source model, fine-tune it on custom data, and deploy it.

---

## What You're Building

A model that's been trained further on your specific data — so it behaves exactly the way you want for a specific task. Fine-tuning is what takes a general model and makes it a specialist.

---

## What You'll Learn

- The difference between prompting, RAG, and fine-tuning — and when to use each
- How to prepare a training dataset
- Running fine-tuning jobs on Hugging Face or OpenAI
- Evaluating whether your fine-tuned model is actually better

---

## When Fine-Tuning Makes Sense

| Use This When... | Don't Use When... |
|------------------|-------------------|
| You need a very specific tone or style | A system prompt would work |
| You have 100s of labeled examples | You only have a few examples |
| Latency and cost matter at scale | You're prototyping |
| The task is highly specialized | RAG would solve it |

---

## Approach

### Step 1 — Prepare Your Dataset
```jsonl
{"messages": [{"role": "user", "content": "Input example"}, {"role": "assistant", "content": "Perfect output"}]}
{"messages": [{"role": "user", "content": "Another input"}, {"role": "assistant", "content": "Another perfect output"}]}
```
You need at least 50–100 examples. More is better.

### Step 2 — Fine-Tune (Two Options)

**Option A — OpenAI (easiest):**
```python
from openai import OpenAI
client = OpenAI()

client.fine_tuning.jobs.create(
    training_file="file-abc123",
    model="gpt-4o-mini"
)
```

**Option B — Hugging Face (free, open-source):**
Use `transformers` + `trl` library with a small model like `mistral-7b` or `llama-3.2-1b`.

### Step 3 — Evaluate
Compare fine-tuned vs base model on 20 test examples. Is it actually better?

---

## Done When

- [ ] Dataset of 50+ examples prepared and formatted correctly
- [ ] Fine-tuning job completes without errors
- [ ] Fine-tuned model performs measurably better than base model on your task

---

## Stretch Goals

- Use LoRA / QLoRA to fine-tune a larger model on limited hardware
- Host your model on Hugging Face Hub
- Build a simple API wrapper around your fine-tuned model
