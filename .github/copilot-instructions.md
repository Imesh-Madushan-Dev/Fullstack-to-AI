# fullstack-to-ai — Copilot Instructions

**Learning-by-building path:** 15 progressive AI projects for developers. No tutorials. No fluff. Just implement, learn, repeat.

---

## Project Tier System

Projects are tiered by difficulty and conceptual prerequisites. **Don't skip levels.**

| Tier         | Icon | Projects | Prerequisites       | Focus                                                        |
| ------------ | ---- | -------- | ------------------- | ------------------------------------------------------------ |
| **Ant**      | 🐜   | #01–03   | Python + API basics | API calls, prompt engineering, structured output             |
| **Rabbit**   | 🐇   | #04–06   | Ant completed       | Conversation state, context windows, RAG intro               |
| **Fox**      | 🦊   | #07–09   | Rabbit completed    | Frontend integration, complex outputs, file handling         |
| **Wolf**     | 🐺   | #10–12   | Fox completed       | Agents, vector DB, production concerns, multi-turn reasoning |
| **Elephant** | 🐘   | #13–15   | Wolf completed      | Multi-agent systems, fine-tuning, full product scope         |

---

## Coding Standards for AI/LLM Projects

### Always Do These

#### 1. **Secrets & API Keys**

- NEVER hardcode API keys in source → use `.env` files (committed as `.env.example`)
- Use `python-dotenv` or environment variables
- Each project's README should document `.env` vars needed

```python
# ✓ Correct
from dotenv import load_dotenv
import os
load_dotenv()
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# ✗ Never do this
ANTHROPIC_API_KEY = "sk-ant-..."  # COMMIT MISTAKE
```

#### 2. **Message History & Context**

- Always store full conversation history (model is stateless)
- Track token usage; warn users when approaching context limits
- Clear conversation history when requested (e.g., `/clear` command)

```python
# ✓ Pattern
messages = [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
response = client.messages.create(model="...", messages=messages)
messages.append({"role": "assistant", "content": response.content[0].text})
```

#### 3. **Error Handling for API Calls**

- Catch `RateLimitError`, `APIError`, `APIConnectionError`
- Show user-friendly messages (never raw exception dumps)
- Log full errors internally for debugging

```python
from anthropic import APIError, RateLimitError

try:
    response = client.messages.create(...)
except RateLimitError:
    print("API is busy. Try again in a moment.")
except APIError as e:
    print(f"Unable to reach AI service. Check internet and try again.")
    logger.error(f"API error: {e}")
```

#### 4. **Prompt Engineering**

- Use system prompts for consistent behavior (vs. embedding instructions in user messages)
- Comments in code: explain **why** a prompt is written that way
- Test prompts with multiple inputs before iteration

```python
SYSTEM_PROMPT = """You are a code reviewer. Focus on: logic, security, readability.
Provide feedback as bullet points with suggestions—not just critiques."""

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    system=SYSTEM_PROMPT,
    messages=messages
)
```

#### 5. **File Handling**

- Always handle missing/invalid files gracefully
- For text files: default to UTF-8, handle encoding errors
- For structured output (JSON, CSV): validate before writing

```python
try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(f"Error: File not found: {filepath}")
except UnicodeDecodeError:
    print(f"Error: File is not valid UTF-8")
```

#### 6. **Logging & Debugging**

- Use `import logging` → `logger = logging.getLogger(__name__)`
- NO `print()` for production logs (use logger)
- `print()` is OK for user-facing interaction only

```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"Processing: {filename}")
logger.debug(f"Full API response: {response}")
logger.error(f"Failed to process: {e}")
```

#### 7. **Requirements & Dependencies**

- Always maintain `requirements.txt` (pinned versions or `^` for 90% of cases)
- Document Python version requirement (3.10+)
- Each project README should include install instructions

```bash
# requirements.txt
anthropic==0.42.0
python-dotenv==1.0.1
requests==2.32.0
```

### NEVER Do These

| ❌                                  | ✅                                       | Reason                                      |
| ----------------------------------- | ---------------------------------------- | ------------------------------------------- |
| `print(exception)` as error handler | `logger.error()` + user-friendly message | Raw traces confuse users; log for debugging |
| Hardcode API keys                   | `.env` + `.env.example`                  | Security; keys get leaked to GitHub         |
| Single-turn API calls without retry | Exponential backoff for `RateLimitError` | Flaky networks; be resilient                |
| Assume model output is valid        | Validate JSON/structure before using     | Models can hallucinate; sanitize output     |
| Leave secrets in comments or prints | Never show API keys anywhere             | Assume terminal output is logged            |
| Ignore context window limits        | Track tokens; warn at ~80%               | Truncated responses confuse users           |

---

## Project Checklist (Every Project)

Use this before moving to the next tier:

- [ ] **Code Quality**
  - [ ] All imports organized (stdlib, 3rd-party, local)
  - [ ] No hardcoded secrets (API keys in `.env`)
  - [ ] Logging configured (not just `print`)
  - [ ] Graceful error handling for API + file operations
  - [ ] Type hints on function signatures (`def fetch(query: str) -> dict:`)

- [ ] **Documentation**
  - [ ] README.md updated with clear instructions
  - [ ] `.env.example` committed (shows required vars)
  - [ ] Code comments on non-obvious prompt logic
  - [ ] Usage example in README (e.g., how to run, expected output)

- [ ] **Testing & Validation**
  - [ ] Manual test: run the project locally
  - [ ] Verify: all "Done When" checklist items pass
  - [ ] Optional: add unit tests for core logic (not required but encouraged)

- [ ] **Git & Tracking**
  - [ ] Commit message references project goal (e.g., `#03: Add structured JSON output`)
  - [ ] No uncommitted `.env` files (add to `.gitignore`)
  - [ ] Clean git history before submitting pull request

---

## Common Patterns Across Projects

### Pattern 1: Message Loop (Ant/Rabbit Projects)

```python
def chat_loop(system_prompt: str):
    client = Anthropic()
    messages = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        )

        assistant_reply = response.content[0].text
        messages.append({"role": "assistant", "content": assistant_reply})
        print(f"\nAssistant: {assistant_reply}\n")
```

### Pattern 2: File Input → API → Output (Fox Projects)

```python
def process_document(filepath: str, query: str) -> str:
    """Load document, send to AI, return analysis."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            document = f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return None

    client = Anthropic()
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=[
            {"role": "user", "content": f"Document:\n\n{document}\n\nQuery: {query}"}
        ]
    )

    return response.content[0].text
```

### Pattern 3: Retry with Backoff (Wolf Projects)

```python
import time
from anthropic import RateLimitError, APIError

def call_with_retry(client, **kwargs) -> dict:
    """Call API with exponential backoff on rate limit."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return client.messages.create(**kwargs)
        except RateLimitError:
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            logger.warning(f"Rate limited. Retrying in {wait_time}s...")
            time.sleep(wait_time)
        except APIError as e:
            logger.error(f"API error: {e}")
            raise
    raise APIError("Max retries exceeded")
```

---

## How Copilot Can Help

When working on a project, ask Copilot to:

- **Implement** a feature by referencing the project README
- **Debug** API errors and explain what went wrong
- **Refactor** code to follow the standards above
- **Test** output by running dummy inputs
- **Document** your approach in comments

### Example Prompts

- `Implement the chat loop for project #05 (AI FAQ Bot). Load FAQs from a JSON file, use RAG to find relevant docs, then answer the user.`
- `I'm getting a RateLimitError. How should I add retry logic here?`
- `Review this prompt. Is it clear? Will the model output structured JSON?`
- `Write a test for the summarizer that validates the output is < 100 tokens.`

---

## Learning Path Progression

### After Ant (Projects #01–03)

- You know API calls, message history, tokens
- **Next tier:** Learn how to keep conversation context between runs

### After Rabbit (Projects #04–06)

- You understand conversation state, simple RAG, context injection
- **Next tier:** Add a UI; stop living in the terminal

### After Fox (Projects #07–09)

- You've integrated UI + file handling + complex outputs
- **Next tier:** Learn agents, vector DB, real production concerns

### After Wolf (Projects #10–12)

- You've built multi-turn reasoning, handled production constraints
- **Next tier:** Scale to teams; fine-tune models

### After Elephant (Projects #13–15)

- You've built end-to-end AI products with agents and custom models
- **Next:** Ship real products; consult on AI features

---

## Resources

- **CLI / Fast**: Install [Anthropic Python SDK](https://docs.anthropic.com/en/api/getting-started)
- **Prompting**: [Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-a-bot)
- **Models**: Always use latest stable (check [models page](https://docs.anthropic.com/en/docs/about/models))
- **Rate Limits**: Monitor usage in your API dashboard
- **Debugging**: Use `logging` module + read responses carefully

---

## Questions?

- Project README unclear? → Open an issue with specifics
- Stuck on a feature? → Ask Copilot to help implement + explain
- Want to skip a tier? → Don't. Each tier teaches prerequisites for the next

**Built by a dev, for devs. Make it yours. Ship it.**
