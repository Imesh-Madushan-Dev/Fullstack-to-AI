import ast
import json
import os
from pathlib import Path
from urllib.parse import quote

from dotenv import load_dotenv
import google.genai as genai
import requests

MODEL_NAME = "gemini-2.5-flash"


def safe_calculate(expression: str) -> str:
    allowed_nodes = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,
        ast.Constant,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.Mod,
        ast.USub,
        ast.UAdd,
        ast.FloorDiv,
    }
    tree = ast.parse(expression, mode="eval")
    for node in ast.walk(tree):
        if type(node) not in allowed_nodes:
            raise ValueError("Expression contains unsupported operations.")
    value = eval(compile(tree, "<expr>", "eval"), {"__builtins__": {}}, {})
    return str(value)


def read_file_tool(path: str) -> str:
    p = Path(path)
    if not p.exists() or not p.is_file():
        return "Error: file not found."
    try:
        return p.read_text(encoding="utf-8")[:4000]
    except Exception:
        return "Error: failed to read file."


def web_search_tool(query: str) -> str:
    try:
        title_url = (
            "https://en.wikipedia.org/w/api.php"
            f"?action=opensearch&search={quote(query)}&limit=1&namespace=0&format=json"
        )
        title_resp = requests.get(title_url, timeout=10)
        title_resp.raise_for_status()
        data = title_resp.json()
        titles = data[1]
        if not titles:
            return "No web result found."

        title = titles[0]
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"
        summary_resp = requests.get(summary_url, timeout=10)
        summary_resp.raise_for_status()
        summary = summary_resp.json().get("extract", "No summary found.")
        return f"Title: {title}\nSummary: {summary}"
    except Exception:
        return "Error: web search failed."


def parse_agent_json(text: str) -> dict | None:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None


def agent_step(client: genai.Client, user_query: str, tool_result: str = "") -> dict | None:
    prompt = f"""
You are an AI agent that can use tools.

Available tools:
1) calculator -> input: math expression string
2) read_file -> input: local file path string
3) web_search -> input: search query string

Return ONLY JSON using one of these formats:
{{"action":"tool","tool":"calculator|read_file|web_search","input":"..."}}
{{"action":"final","answer":"..."}}

User query: {user_query}
Previous tool result (if any): {tool_result or "none"}
""".strip()

    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return parse_agent_json(response.text or "")


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Create .env from .env.example.")
        return

    client = genai.Client(api_key=api_key)

    print("AI Agent with Tools")
    print("Type a question. Type /exit to quit.\n")

    while True:
        user_query = input("You: ").strip()
        if user_query == "/exit":
            print("Goodbye!")
            break
        if not user_query:
            continue

        tool_result = ""
        answered = False

        for _ in range(3):
            decision = agent_step(client, user_query, tool_result)
            if not decision:
                break

            action = decision.get("action")
            if action == "final":
                print(f"\nAgent: {decision.get('answer', 'No answer generated.')}\n")
                answered = True
                break

            if action == "tool":
                tool = str(decision.get("tool", "")).strip()
                tool_input = str(decision.get("input", "")).strip()
                print(f"\n[Tool call] {tool} -> {tool_input}")

                if tool == "calculator":
                    try:
                        tool_result = safe_calculate(tool_input)
                    except Exception as e:
                        tool_result = f"Error: {e}"
                elif tool == "read_file":
                    tool_result = read_file_tool(tool_input)
                elif tool == "web_search":
                    tool_result = web_search_tool(tool_input)
                else:
                    tool_result = "Error: unknown tool."

                print(f"[Tool result] {tool_result[:300]}\n")
                continue

            break

        if answered:
            continue

        fallback_prompt = (
            f"Answer this user query directly in a helpful way:\n{user_query}\n"
            f"If relevant, include this tool result:\n{tool_result}"
        )
        try:
            fallback = client.models.generate_content(model=MODEL_NAME, contents=fallback_prompt)
            print(f"\nAgent: {(fallback.text or 'No answer generated.').strip()}\n")
        except Exception:
            print("\nAgent: Error: could not generate response.\n")


if __name__ == "__main__":
    main()
