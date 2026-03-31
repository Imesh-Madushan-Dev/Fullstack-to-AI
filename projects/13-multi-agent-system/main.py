import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import google.genai as genai

MODEL_NAME = "gemini-2.5-flash"

RESEARCHER_PROMPT = "You are a researcher. Return factual bullet notes with key data points."
WRITER_PROMPT = "You are a writer. Turn research notes into a clear report draft with sections."
EDITOR_PROMPT = "You are an editor. Improve clarity, structure, and completeness. Return polished final report."


def run_agent(client: genai.Client, system_prompt: str, task_input: str) -> str:
    prompt = f"""
{system_prompt}

Task input:
{task_input}
""".strip()
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return (response.text or "").strip()


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Create .env from .env.example.")
        return

    topic = input("Enter report topic: ").strip()
    if not topic:
        print("Topic is required.")
        return

    client = genai.Client(api_key=api_key)

    print("\n[1/3] Researcher agent working...")
    notes = run_agent(client, RESEARCHER_PROMPT, topic)

    print("[2/3] Writer agent working...")
    draft = run_agent(client, WRITER_PROMPT, notes)

    print("[3/3] Editor agent working...")
    final_report = run_agent(client, EDITOR_PROMPT, draft)

    print("\n=== FINAL REPORT ===\n")
    print(final_report)

    save = input("\nSave report to file? (y/n): ").strip().lower()
    if save == "y":
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        Path(filename).write_text(final_report, encoding="utf-8")
        print(f"Saved: {filename}")


if __name__ == "__main__":
    main()
