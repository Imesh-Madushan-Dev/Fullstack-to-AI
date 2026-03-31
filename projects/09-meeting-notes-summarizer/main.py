import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import google.genai as genai

MODEL_NAME = "gemini-2.5-flash"


def read_transcript() -> str:
    print("Choose transcript input:")
    print("1) Paste transcript")
    print("2) Read from file")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        print("Paste transcript. Type END on a new line when done:\n")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        return "\n".join(lines).strip()

    if choice == "2":
        path = input("Transcript file path: ").strip()
        try:
            return Path(path).read_text(encoding="utf-8")
        except FileNotFoundError:
            print("Error: file not found.")
        except UnicodeDecodeError:
            print("Error: file is not valid UTF-8.")

    return ""


def build_prompt(transcript: str) -> str:
    return f"""
Analyze this meeting transcript and return:
1) SUMMARY (max 3 sentences)
2) DECISIONS MADE (bullet list)
3) ACTION ITEMS (format: Person -> Task -> Deadline if mentioned)

If anything is unclear, say "Unclear" instead of guessing.

Transcript:
{transcript}
""".strip()


def maybe_export(content: str) -> None:
    save = input("\nSave output to a file? (y/n): ").strip().lower()
    if save != "y":
        return

    filename = f"meeting_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    Path(filename).write_text(content, encoding="utf-8")
    print(f"Saved: {filename}")


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Create .env from .env.example.")
        return

    transcript = read_transcript()
    if not transcript:
        print("No transcript provided.")
        return

    client = genai.Client(api_key=api_key)
    prompt = build_prompt(transcript)

    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        result = (response.text or "No output generated.").strip()
    except Exception:
        print("Error: failed to summarize transcript.")
        return

    print("\n=== Meeting Summary ===\n")
    print(result)
    maybe_export(result)


if __name__ == "__main__":
    main()
