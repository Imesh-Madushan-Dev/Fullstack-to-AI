<div align="center">

# 🧠 fullstack-to-ai

**A structured, project-based journey from full-stack developer to AI engineer.**  
Built by a dev, for devs. No fluff. No theory overload. Just build.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Projects](https://img.shields.io/badge/Projects-15-blue)
![Level](https://img.shields.io/badge/Level-Beginner%20→%20Advanced-green)
![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Claude%20%7C%20OpenAI-orange)

</div>

---

## 👋 Hey, you found this repo

This is my personal learning path for becoming an AI engineer — built while I was making the transition from full-stack development.

I structured it so that **anyone with a dev background** can follow along, fork it, and use it as their own roadmap. Every project has a clear goal, an approach, a checklist, and stretch goals.

**Who this is for:**
- Full-stack devs who want to break into AI engineering
- Anyone who learns by building, not watching tutorials
- People who want a no-fluff, progressive path with real projects

---

## 🍴 How to Use This Repo

**Fork it. Make it yours.**

```bash
# 1. Fork this repo on GitHub (top right button)

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/fullstack-to-ai.git
cd fullstack-to-ai

# 3. Start at Project 01 and work your way up
cd 02-projects/ant/01-ai-chat-terminal
cat README.md
```

> **The rule:** Don't skip levels. Each project teaches something the next one depends on.

---

## 🗺️ The Path

```
fullstack-to-ai/
├── 01-foundations/        # Core concepts + setup checklist
├── 02-projects/
│   ├── 🐜 ant/            # Beginner — get your feet wet
│   ├── 🐇 rabbit/         # Getting comfortable
│   ├── 🦊 fox/            # Building real things
│   ├── 🐺 wolf/           # You're dangerous now
│   └── 🐘 elephant/       # Full AI engineer level
├── 03-notes/              # My personal notes as I build
└── 04-resources/          # Curated tools and links
```

---

## 🏗️ The 15 Projects

### 🐜 Ant — Get Your Feet Wet
*Learn the basics. Make your first API calls. Don't overthink it.*

| # | Project | What You Learn | Time |
|---|---------|----------------|------|
| 01 | [AI Chat in Terminal](02-projects/01-ai-chat-terminal/) | API calls, message history, tokens | 2–4h |
| 02 | [Text Summarizer](02-projects/02-text-summarizer/) | Prompt engineering, output control | 1–2h |
| 03 | [Mood Detector](02-projects/03-mood-detector/) | Structured outputs, classification | 1–2h |

### 🐇 Rabbit — Getting Comfortable
*Start handling real data. Learn how memory and context actually work.*

| # | Project | What You Learn | Time |
|---|---------|----------------|------|
| 04 | [Chatbot with Memory](02-projects/04-chatbot-with-memory/) | Conversation state, context windows | 3–5h |
| 05 | [AI FAQ Bot](02-projects/05-ai-faq-bot/) | RAG basics, context injection | 4–6h |
| 06 | [AI Code Reviewer](02-projects/06-ai-code-reviewer/) | Domain-specific prompting | 3–5h |

### 🦊 Fox — Building Real Things
*Add a UI. Handle files. Build something a real person could use.*

| # | Project | What You Learn | Time |
|---|---------|----------------|------|
| 07 | [Chatbot with UI](02-projects/07-chatbot-with-ui/) | AI + frontend integration, streaming | 4–8h |
| 08 | [Document Q&A App](02-projects/08-document-qa-app/) | PDF handling, embeddings intro | 6–10h |
| 09 | [Meeting Notes Summarizer](02-projects/09-meeting-notes-summarizer/) | Complex structured output, export | 4–6h |

### 🐺 Wolf — You're Dangerous Now
*Agents. Vector databases. Real users. Production concerns.*

| # | Project | What You Learn | Time |
|---|---------|----------------|------|
| 10 | [AI Agent with Tools](02-projects/10-ai-agent-with-tools/) | Tool calling, agentic loops | 8–12h |
| 11 | [Full RAG Pipeline](02-projects/11-full-rag-pipeline/) | Vector DBs, semantic search at scale | 10–16h |
| 12 | [AI-Powered SaaS Feature](02-projects/12-ai-powered-saas-feature/) | Production AI, real users | 10–20h |

### 🐘 Elephant — AI Engineer Level
*Multi-agent systems. Fine-tuning. A shipped product.*

| # | Project | What You Learn | Time |
|---|---------|----------------|------|
| 13 | [Multi-Agent System](02-projects/13-multi-agent-system/) | Agent orchestration, LangGraph | 16–24h |
| 14 | [Fine-Tuned Model](02-projects/14-fine-tuned-model/) | Fine-tuning, Hugging Face, evals | 20–40h |
| 15 | [End-to-End AI Product](02-projects/15-end-to-end-ai-product/) | Everything. Shipped. | 40–80h |

> **Total estimated time:** 130–240 hours depending on pace and stretch goals.

---

## ⚡ Quick Start (Your First Hour)

```bash
# Install Python if you haven't
python --version  # needs 3.10+

# Install the Anthropic SDK
pip install anthropic python-dotenv

# Create your .env file
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Get your API key at console.anthropic.com (free tier available)
# Then start Project 01
cd 02-projects/ant/01-ai-chat-terminal
```

---

## 🛠️ Stack

| Layer | Tools |
|-------|-------|
| Language | Python (primary), JavaScript (where needed) |
| LLM APIs | Anthropic Claude, OpenAI |
| Frameworks | LangChain, LlamaIndex |
| Vector DBs | ChromaDB (local), Pinecone (hosted) |
| UI | Streamlit (quick), or your existing JS stack |
| Models | Hugging Face (open source, fine-tuning) |

---

## 📋 Ground Rules

1. **Don't skip levels.** Each project teaches something the next depends on.
2. **Build first, perfect later.** A working ugly thing beats a perfect idea.
3. **Document as you go.** Use `03-notes/` — future you will be grateful.
4. **Make it your own.** Fork this, rename things, build projects that interest *you*.

---

## 🤝 Contributing

Found a bug in a project guide? Have a better approach? PRs welcome.

1. Fork the repo
2. Create a branch: `git checkout -b improve/project-05`
3. Make your changes
4. Open a PR with a clear description

---

## 📄 License

MIT — fork it, use it, share it.

---

<div align="center">

**If this helped you, give it a ⭐ — it helps others find it.**

*Started 2026 · Background: Full-stack developer → AI engineer in progress*

</div>