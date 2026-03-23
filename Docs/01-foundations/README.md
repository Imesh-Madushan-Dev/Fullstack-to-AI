# Foundations

Core concepts to understand before diving into projects.  
You don't need to memorize these — just be familiar enough to not feel lost.

---

## Concepts to Know

### How LLMs Work
- Input is broken into **tokens** (not words, not characters — somewhere in between)
- The model predicts the next token based on context
- **Temperature** controls randomness — 0 = deterministic, 1+ = creative/chaotic
- **Context window** = how much text the model can "see" at once

### Key Terms

| Term | What It Means |
|------|---------------|
| Prompt | The input you send to the model |
| Completion | The model's response |
| System prompt | Instructions that shape the model's behavior |
| Embedding | A number representation of text (used for search) |
| RAG | Retrieval-Augmented Generation — giving the model extra context from your data |
| Fine-tuning | Training the model further on your specific data |
| Agent | An AI that can take actions, not just respond |
| Tool calling | Giving the model the ability to run functions |

---

## Setup Checklist

- [ ] Python installed (3.10+)
- [ ] `pip` working
- [ ] Anthropic API key → [console.anthropic.com](https://console.anthropic.com)
- [ ] OpenAI API key (optional backup) → [platform.openai.com](https://platform.openai.com)
- [ ] API keys saved in `.env` file (never hardcode them)

### Basic `.env` setup
```
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

### Load it in Python
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
```

---

## Resources That Actually Help

- [Anthropic Docs](https://docs.anthropic.com) — read like framework docs
- [Andrej Karpathy — Neural Networks: Zero to Hero](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ) — best deep dive on YouTube
- [fast.ai](https://fast.ai) — practical, code-first ML course
- [Simon Willison's Blog](https://simonwillison.net) — real-world AI engineering
