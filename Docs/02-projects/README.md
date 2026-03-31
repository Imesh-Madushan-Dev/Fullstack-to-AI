# Projects

15 projects organized by difficulty. Each one teaches you something the next depends on.  
**Don't skip levels.**

---

## Shared Environment Workflow

Use one shared virtual environment for all projects in this repo.

1. From workspace root, run:

```powershell
./setup-shared-env.ps1
```

2. Activate environment in each new terminal:

```powershell
.\venv\Scripts\Activate.ps1
```

3. Run a project by number:

```powershell
./run-project.ps1 1
./run-project.ps1 2
./run-project.ps1 3
```

4. Or run by folder name (inside `projects/`):

```powershell
./run-project.ps1 01-ai-chat-terminal
./run-project.ps1 02-text-summarizer
./run-project.ps1 03-mood-detector
```

Notes:

- `setup-shared-env.ps1` creates `venv/` only once, then reuses it.
- `requirements-shared.txt` is the shared dependency list.
- Keep each project's own `requirements.txt` for project-level reference.

---

## 🐜 Ant — Get Your Feet Wet

| #   | Project                                         | Time | Key Skill                  |
| --- | ----------------------------------------------- | ---- | -------------------------- |
| 01  | [AI Chat in Terminal](ant/01-ai-chat-terminal/) | 2–4h | API calls, message history |
| 02  | [Text Summarizer](ant/02-text-summarizer/)      | 1–2h | Prompt engineering         |
| 03  | [Mood Detector](ant/03-mood-detector/)          | 1–2h | Structured outputs         |

---

## 🐇 Rabbit — Getting Comfortable

| #   | Project                                               | Time | Key Skill                     |
| --- | ----------------------------------------------------- | ---- | ----------------------------- |
| 04  | [Chatbot with Memory](rabbit/04-chatbot-with-memory/) | 3–5h | Conversation state            |
| 05  | [AI FAQ Bot](rabbit/05-ai-faq-bot/)                   | 4–6h | RAG basics, context injection |
| 06  | [AI Code Reviewer](rabbit/06-ai-code-reviewer/)       | 3–5h | Domain-specific prompting     |

---

## 🦊 Fox — Building Real Things

| #   | Project                                                      | Time  | Key Skill                      |
| --- | ------------------------------------------------------------ | ----- | ------------------------------ |
| 07  | [Chatbot with UI](fox/07-chatbot-with-ui/)                   | 4–8h  | AI + frontend integration      |
| 08  | [Document Q&A App](fox/08-document-qa-app/)                  | 6–10h | PDF handling, embeddings intro |
| 09  | [Meeting Notes Summarizer](fox/09-meeting-notes-summarizer/) | 4–6h  | Complex structured output      |

---

## 🐺 Wolf — You're Dangerous Now

| #   | Project                                                     | Time   | Key Skill                   |
| --- | ----------------------------------------------------------- | ------ | --------------------------- |
| 10  | [AI Agent with Tools](wolf/10-ai-agent-with-tools/)         | 8–12h  | Tool calling, agentic loops |
| 11  | [Full RAG Pipeline](wolf/11-full-rag-pipeline/)             | 10–16h | Vector DBs, semantic search |
| 12  | [AI-Powered SaaS Feature](wolf/12-ai-powered-saas-feature/) | 10–20h | Production AI, real users   |

---

## 🐘 Elephant — AI Engineer Level

| #   | Project                                                     | Time   | Key Skill                   |
| --- | ----------------------------------------------------------- | ------ | --------------------------- |
| 13  | [Multi-Agent System](elephant/13-multi-agent-system/)       | 16–24h | Agent orchestration         |
| 14  | [Fine-Tuned Model](elephant/14-fine-tuned-model/)           | 20–40h | Fine-tuning, model training |
| 15  | [End-to-End AI Product](elephant/15-end-to-end-ai-product/) | 40–80h | Everything, shipped         |

---

_Total estimated time: 130–240 hours depending on pace and stretch goals._
