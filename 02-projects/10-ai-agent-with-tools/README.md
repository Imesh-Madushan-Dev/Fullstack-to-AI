# 10 — AI Agent with Tools

**Level:** 🐺 Wolf  
**Time:** 8–12 hours  
**Goal:** Build an AI that decides which tool to use — web search, file reading, or direct answer.

---

## What You're Building

Your first real agent. Unlike a chatbot (which only responds), an agent can take actions. You give it tools, and it decides which one to use based on your question.

---

## What You'll Learn

- Tool calling / function calling — how to give the model "hands"
- Agentic loops — model decides → action runs → model sees result → responds
- How agents can fail and how to handle errors

---

## Approach

1. Define tools as functions (web search, read file, calculate)
2. Pass tool definitions to the API
3. If the model returns a tool call, run the function
4. Send the result back to the model
5. Model gives final answer

```python
# Define tools for the model
tools = [
    {
        "name": "web_search",
        "description": "Search the web for current information",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    }
]

# The model will return tool_use blocks when it wants to use a tool
response = client.messages.create(
    model="claude-opus-4-5",
    tools=tools,
    messages=messages
)

# Check if model wants to use a tool
if response.stop_reason == "tool_use":
    # Run the tool, send result back
    pass
```

---

## Done When

- [ ] Agent correctly chooses between at least 2 tools
- [ ] Tool results feed back into the model's final answer
- [ ] Handles the case where a tool fails or returns nothing

---

## Stretch Goals

- Add a calculator tool (evaluate math expressions)
- Add a "read file" tool that can access local files
- Log every tool call so you can see the agent's reasoning
