import os
from pathlib import Path

from dotenv import load_dotenv
import google.genai as genai

MODEL_NAME = "gemini-2.5-flash"


def read_text_from_terminal() -> str:
    print("\nPaste your text below. Type END on a new line when done:\n")
    lines = []

    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    return "\n".join(lines).strip()


def read_text_from_file() -> str:
    file_path = input("Enter .txt file path: ").strip()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("Error: file not found.")
    except UnicodeDecodeError:
        print("Error: file is not valid UTF-8 text.")

    return ""


def choose_text_input() -> str:
    print("Choose input method:")
    print("1) Paste text")
    print("2) Read from .txt file")

    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        return read_text_from_terminal()
    if choice == "2":
        return read_text_from_file()

    print("Invalid choice.")
    return ""


def choose_summary_length() -> str:
    print("\nChoose summary length:")
    print("1) Short")
    print("2) Medium")
    print("3) Detailed")

    choice = input("Enter 1, 2, or 3: ").strip()

    if choice == "1":
        return "short"
    if choice == "2":
        return "medium"
    if choice == "3":
        return "detailed"

    print("Invalid choice. Using short.")
    return "short"


def build_prompt(text: str, summary_length: str) -> str:
    return (
        "Summarize the text below in exactly 3 bullet points. "
        "Each bullet should be one sentence and easy to understand. "
        f"Make the summary {summary_length}.\n\n"
        "TEXT:\n"
        f"{text}"
    )


def save_summary(summary: str) -> None:
    save_choice = input("\nSave summary to summary.txt? (y/n): ").strip().lower()
    if save_choice != "y":
        return

    output_path = Path("summary.txt")
    output_path.write_text(summary, encoding="utf-8")
    print(f"Saved to {output_path}")


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY not found. Create a .env file first.")
        print("Tip: copy .env.example to .env and add your key.")
        return

    text = choose_text_input()
    if not text:
        print("No text received. Exiting.")
        return

    summary_length = choose_summary_length()
    prompt = build_prompt(text, summary_length)

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
    except Exception:
        print("Error: failed to get a response from Gemini.")
        return

    summary = response.text or "(No summary returned)"

    print("\nSummary:\n")
    print(summary)

    save_summary(summary)


if __name__ == "__main__":
    main()
