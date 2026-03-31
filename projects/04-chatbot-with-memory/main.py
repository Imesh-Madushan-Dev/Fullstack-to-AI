import os

from dotenv import load_dotenv
import google.genai as genai

MODEL_NAME = "gemini-2.5-flash"
SYSTEM_PROMPT = (
    "You are a helpful assistant. Keep answers clear and practical. "
    "Remember details from previous user messages in this chat."
)


def rough_token_count(text: str) -> int:
    return max(1, len(text) // 4)


def format_history(messages: list[dict[str, str]]) -> str:
    if not messages:
        return "(no history yet)"
    lines = []
    for msg in messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        lines.append(f"{role}: {msg['content']}")
    return "\n".join(lines)


def build_prompt(messages: list[dict[str, str]]) -> str:
    return (
        f"System instructions:\n{SYSTEM_PROMPT}\n\n"
        "Conversation so far:\n"
        f"{format_history(messages)}\n\n"
        "Continue the conversation naturally."
    )


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found. Create .env from .env.example.")
        return

    client = genai.Client(api_key=api_key)
    messages: list[dict[str, str]] = []

    print("CLI Chatbot with Memory")
    print("Commands: /clear, /history, /exit\n")

    while True:
        user_input = input("You: ").strip()

        if user_input == "/exit":
            print("Goodbye!")
            break
        if user_input == "/clear":
            messages.clear()
            print("Conversation cleared.\n")
            continue
        if user_input == "/history":
            print("\n--- Conversation History ---")
            print(format_history(messages))
            print("----------------------------\n")
            continue
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        prompt = build_prompt(messages)

        token_estimate = rough_token_count(prompt)
        if token_estimate > 6000:
            print("Warning: context is getting long. Consider /clear soon.\n")

        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
            reply = (response.text or "Sorry, I could not generate a reply.").strip()
        except Exception:
            print("Error: API call failed. Try again.\n")
            messages.pop()
            continue

        messages.append({"role": "assistant", "content": reply})
        print(f"\nAI: {reply}")
        print(f"[approx tokens in context: {token_estimate}]\n")


if __name__ == "__main__":
    main()
