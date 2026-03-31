import os
from pathlib import Path

from dotenv import load_dotenv
import google.genai as genai

MODEL_NAME = "gemini-2.5-flash"


def read_code_from_terminal() -> str:
    print("Paste code below. Type END on a new line when done:\n")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def read_code_from_file() -> str:
    path = input("Enter code file path: ").strip()
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        print("Error: file not found.")
    except UnicodeDecodeError:
        print("Error: file is not valid UTF-8.")
    return ""


def choose_input() -> str:
    print("1) Paste code")
    print("2) Read from file")
    choice = input("Choose input method (1/2): ").strip()
    if choice == "1":
        return read_code_from_terminal()
    if choice == "2":
        return read_code_from_file()
    print("Invalid choice.")
    return ""


def review_code(client: genai.Client, code: str, style: str) -> str:
    prompt = f"""
You are a senior software engineer reviewing code.
Tone style: {style}.

Return output with exactly these sections:
1) BUGS
2) IMPROVEMENTS
3) READABILITY
4) SCORE (1-10)

Be specific. Prefer actionable fixes.

Code:
{code}
""".strip()

    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return (response.text or "No review generated.").strip()


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Create .env from .env.example.")
        return

    code = choose_input()
    if not code:
        print("No code provided.")
        return

    style = input("Review style (strict/friendly, default strict): ").strip().lower() or "strict"
    if style not in {"strict", "friendly"}:
        style = "strict"

    client = genai.Client(api_key=api_key)
    try:
        review = review_code(client, code, style)
    except Exception:
        print("Error: review request failed.")
        return

    print("\n=== Review ===\n")
    print(review)


if __name__ == "__main__":
    main()
