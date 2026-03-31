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

# 3. Read the project guide first
cd Docs/02-projects/01-ai-chat-terminal
cat README.md

# 4. Run the actual solution code
cd ../../../projects/01-ai-chat-terminal
python main.py
```

> **The rule:** Don't skip levels. Each project teaches something the next one depends on.

---

## 🗺️ The Path

```
fullstack-to-ai/
├── Docs/
│   ├── 01-foundations/    # Core concepts + setup checklist
│   ├── 02-projects/       # All 15 project guides (what to build)
│   ├── 03-notes/          # Learning notes
│   └── 04-resources/      # Curated tools and links
├── projects/              # Actual runnable code for all 15 projects
├── requirements-shared.txt
├── setup-shared-env.ps1
└── run-project.ps1
```

---

## 🏗️ The 15 Projects

### 🐜 Ant — Get Your Feet Wet

_Learn the basics. Make your first API calls. Don't overthink it._

| #   | Project                                                      | What You Learn                     | Time |
| --- | ------------------------------------------------------------ | ---------------------------------- | ---- |
| 01  | [AI Chat in Terminal](Docs/02-projects/01-ai-chat-terminal/) | API calls, message history, tokens | 2–4h |
| 02  | [Text Summarizer](Docs/02-projects/02-text-summarizer/)      | Prompt engineering, output control | 1–2h |
| 03  | [Mood Detector](Docs/02-projects/03-mood-detector/)          | Structured outputs, classification | 1–2h |

### 🐇 Rabbit — Getting Comfortable

_Start handling real data. Learn how memory and context actually work._

| #   | Project                                                         | What You Learn                      | Time |
| --- | --------------------------------------------------------------- | ----------------------------------- | ---- |
| 04  | [Chatbot with Memory](Docs/02-projects/04-chatbot-with-memory/) | Conversation state, context windows | 3–5h |
| 05  | [AI FAQ Bot](Docs/02-projects/05-ai-faq-bot/)                   | RAG basics, context injection       | 4–6h |
| 06  | [AI Code Reviewer](Docs/02-projects/06-ai-code-reviewer/)       | Domain-specific prompting           | 3–5h |

### 🦊 Fox — Building Real Things

_Add a UI. Handle files. Build something a real person could use._

| #   | Project                                                                   | What You Learn                       | Time  |
| --- | ------------------------------------------------------------------------- | ------------------------------------ | ----- |
| 07  | [Chatbot with UI](Docs/02-projects/07-chatbot-with-ui/)                   | AI + frontend integration, streaming | 4–8h  |
| 08  | [Document Q&A App](Docs/02-projects/08-document-qa-app/)                  | PDF handling, embeddings intro       | 6–10h |
| 09  | [Meeting Notes Summarizer](Docs/02-projects/09-meeting-notes-summarizer/) | Complex structured output, export    | 4–6h  |

### 🐺 Wolf — You're Dangerous Now

_Agents. Vector databases. Real users. Production concerns._

| #   | Project                                                                 | What You Learn                       | Time   |
| --- | ----------------------------------------------------------------------- | ------------------------------------ | ------ |
| 10  | [AI Agent with Tools](Docs/02-projects/10-ai-agent-with-tools/)         | Tool calling, agentic loops          | 8–12h  |
| 11  | [Full RAG Pipeline](Docs/02-projects/11-full-rag-pipeline/)             | Vector DBs, semantic search at scale | 10–16h |
| 12  | [AI-Powered SaaS Feature](Docs/02-projects/12-ai-powered-saas-feature/) | Production AI, real users            | 10–20h |

### 🐘 Elephant — AI Engineer Level

_Multi-agent systems. Fine-tuning. A shipped product._

| #   | Project                                                             | What You Learn                   | Time   |
| --- | ------------------------------------------------------------------- | -------------------------------- | ------ |
| 13  | [Multi-Agent System](Docs/02-projects/13-multi-agent-system/)       | Agent orchestration, LangGraph   | 16–24h |
| 14  | [Fine-Tuned Model](Docs/02-projects/14-fine-tuned-model/)           | Fine-tuning, Hugging Face, evals | 20–40h |
| 15  | [End-to-End AI Product](Docs/02-projects/15-end-to-end-ai-product/) | Everything. Shipped.             | 40–80h |

> **Total estimated time:** 130–240 hours depending on pace and stretch goals.

---

## ⚡ Quick Start (Run Any Project)

```powershell
# Install Python if you haven't
python --version  # needs 3.10+

# 1) Create one shared virtual environment at repo root
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2) Install shared dependencies for all projects
pip install -r requirements-shared.txt

# 3) Create .env for each project you run (example: project 01)
copy projects\01-ai-chat-terminal\.env.example projects\01-ai-chat-terminal\.env

# 4) Edit that .env and set GEMINI_API_KEY

# 5) Run any project by number
.\run-project.ps1 1
.\run-project.ps1 2
.\run-project.ps1 10
```

Manual alternative:

```powershell
.\venv\Scripts\Activate.ps1
python projects\02-text-summarizer\main.py
```

---

## 🛠️ Stack

| Layer      | Tools                                        |
| ---------- | -------------------------------------------- |
| Language   | Python (primary), JavaScript (where needed)  |
| LLM APIs   | Google Gemini API                            |
| Frameworks | LangChain, LlamaIndex                        |
| Vector DBs | ChromaDB (local), Pinecone (hosted)          |
| UI         | Streamlit (quick), or your existing JS stack |
| Models     | Hugging Face (open source, fine-tuning)      |

---

## 📋 Ground Rules

1. **Don't skip levels.** Each project teaches something the next depends on.
2. **Build first, perfect later.** A working ugly thing beats a perfect idea.
3. **Document as you go.** Use `03-notes/` — future you will be grateful.
4. **Make it your own.** Fork this, rename things, build projects that interest _you_.

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

_Started 2026 · Background: Full-stack developer → AI engineer in progress_

</div>
