import json
import os
from typing import Any

from dotenv import load_dotenv
import google.genai as genai

MODEL_NAME = "gemini-2.5-flash"
ALLOWED_MOODS = ["positive", "negative", "neutral", "excited", "frustrated", "sad"]


def extract_json_object(text: str) -> dict[str, Any] | None:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None


def classify_mood(client: genai.Client, sentence: str) -> tuple[str, int]:
    prompt = f"""
Classify the mood of this sentence.

Return ONLY valid JSON in this format:
{{"mood":"one_label","confidence":7}}

Allowed labels: {", ".join(ALLOWED_MOODS)}
Confidence must be an integer from 1 to 10.

Sentence: "{sentence}"
""".strip()

    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    raw = (response.text or "").strip()
    data = extract_json_object(raw)

    if not data:
        return "neutral", 5

    mood = str(data.get("mood", "neutral")).strip().lower()
    if mood not in ALLOWED_MOODS:
        mood = "neutral"

    confidence_raw = data.get("confidence", 5)
    try:
        confidence = int(confidence_raw)
    except (TypeError, ValueError):
        confidence = 5
    confidence = max(1, min(10, confidence))
    return mood, confidence


def main() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY not found. Create .env from .env.example.")
        return

    client = genai.Client(api_key=api_key)

    print("Mood Detector")
    print("Type a sentence. Type 'exit' to quit.\n")

    while True:
        sentence = input("You: ").strip()
        if sentence.lower() == "exit":
            print("Goodbye!")
            break
        if not sentence:
            continue

        try:
            mood, confidence = classify_mood(client, sentence)
            print(f"Mood: {mood} (confidence: {confidence}/10)\n")
        except Exception:
            print("Error: could not classify mood right now. Try again.\n")


if __name__ == "__main__":
    main()
