# 09 — AI Meeting Notes Summarizer

**Level:** 🦊 Fox  
**Time:** 4–6 hours  
**Goal:** Paste a meeting transcript → get action items, decisions, and a summary.

---

## What You're Building

A practical tool for real work. Paste a raw meeting transcript and get a structured output: who decided what, what needs to happen next, and a 3-sentence summary.

---

## What You'll Learn

- Complex structured output — extracting multiple types of information in one pass
- Real-world prompt engineering — edge cases, messy input, inconsistent formatting
- Output export — generating something the user can actually use

---

## Approach

1. Accept a raw transcript as input (paste or file)
2. Write a prompt that extracts three specific things: summary, decisions, action items
3. Format the output cleanly
4. Add an option to export as a `.txt` or `.md` file

```python
# Core prompt structure
prompt = f"""
Analyze this meeting transcript and extract:

1. SUMMARY (3 sentences max)
2. DECISIONS MADE (list, be specific)
3. ACTION ITEMS (format: "Person → Task → Deadline if mentioned")

If something is unclear, say so. Don't invent details.

TRANSCRIPT:
{transcript}
"""
```

---

## Done When

- [ ] Produces a clean summary from a real meeting transcript
- [ ] Action items list is specific and accurate
- [ ] Output can be exported as a file

---

## Stretch Goals

- Auto-detect speaker names from the transcript
- Generate a follow-up email draft from the action items
- Build a simple UI with file drag-and-drop
