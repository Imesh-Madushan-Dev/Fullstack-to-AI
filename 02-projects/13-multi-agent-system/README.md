# 13 — Multi-Agent System

**Level:** 🐘 Elephant  
**Time:** 16–24 hours  
**Goal:** Multiple AI agents working together — one researches, one writes, one reviews.

---

## What You're Building

A pipeline of specialized agents that hand off work to each other. Each agent is good at one thing. Together, they produce output no single agent could do as well alone.

---

## What You'll Learn

- Agent orchestration — how agents communicate and hand off tasks
- Specialization — different system prompts create different "personalities"
- LangGraph or CrewAI for managing agent workflows
- How multi-agent systems fail (and they do fail — often)

---

## Example Pipeline: Research Report Generator

```
User: "Write a report on solar energy trends"
    ↓
[Researcher Agent] — searches web, gathers facts, returns structured notes
    ↓
[Writer Agent] — turns notes into a readable draft
    ↓
[Editor Agent] — reviews draft, checks for gaps, suggests improvements
    ↓
[Final Report]
```

---

## Approach

**Simple version — Sequential (no framework):**
```python
# Each agent is just a function with its own system prompt
def researcher(topic):
    # System prompt: "You are a research expert..."
    return research_notes

def writer(notes):
    # System prompt: "You are a professional writer..."
    return draft

def editor(draft):
    # System prompt: "You are a critical editor..."
    return final_report

# Chain them
notes = researcher("solar energy trends")
draft = writer(notes)
final = editor(draft)
```

**Advanced version — Use LangGraph or CrewAI for loops and branching.**

---

## Done When

- [ ] At least 3 agents with different roles and system prompts
- [ ] Output from one agent feeds correctly into the next
- [ ] Final output is noticeably better than what a single agent produces

---

## Stretch Goals

- Add a feedback loop — editor can send the draft back to the writer
- Add a human-in-the-loop step — pause and ask for approval before continuing
- Try CrewAI or LangGraph for more complex orchestration
