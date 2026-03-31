import json
import os
from pathlib import Path

from dotenv import load_dotenv
import google.genai as genai

MODEL_NAME = "gemini-2.5-flash"


def validate_jsonl(path: str) -> tuple[bool, list[str]]:
    errors = []
    p = Path(path)
    if not p.exists():
        return False, ["File not found."]

    lines = p.read_text(encoding="utf-8").splitlines()
    if not lines:
        return False, ["File is empty."]

    for i, line in enumerate(lines, start=1):
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"Line {i}: invalid JSON")
            continue

        msgs = item.get("messages")
        if not isinstance(msgs, list) or len(msgs) < 2:
            errors.append(f"Line {i}: 'messages' must be a list with at least 2 entries")
            continue

        roles = {m.get("role") for m in msgs if isinstance(m, dict)}
        if "user" not in roles or "assistant" not in roles:
            errors.append(f"Line {i}: must include both user and assistant messages")

    return len(errors) == 0, errors


def evaluate_base_model(client: genai.Client, path: str, sample_count: int = 3) -> None:
    lines = Path(path).read_text(encoding="utf-8").splitlines()[:sample_count]
    print("\n=== Base Model Quick Evaluation ===")
    for i, line in enumerate(lines, start=1):
        item = json.loads(line)
        user_msg = next(m["content"] for m in item["messages"] if m["role"] == "user")
        expected = next(m["content"] for m in item["messages"] if m["role"] == "assistant")

        resp = client.models.generate_content(model=MODEL_NAME, contents=user_msg)
        actual = (resp.text or "").strip()

        print(f"\nSample {i}")
        print(f"Prompt: {user_msg}")
        print(f"Expected style/output: {expected}")
        print(f"Base model output: {actual}")


def main() -> None:
    print("Fine-Tuned Model Project Helper")
    print("1) Validate training JSONL")
    print("2) Validate + quick base-model evaluation")
    choice = input("Choose option (1/2): ").strip()

    dataset_path = input("Enter JSONL path (default sample_train.jsonl): ").strip() or "sample_train.jsonl"
    is_valid, errors = validate_jsonl(dataset_path)

    if not is_valid:
        print("\nValidation failed:")
        for err in errors:
            print(f"- {err}")
        return

    print("\nValidation passed.")

    if choice != "2":
        print("Next step: upload dataset to your fine-tuning provider (OpenAI/Hugging Face).")
        return

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY missing. Skipping evaluation.")
        return

    client = genai.Client(api_key=api_key)
    try:
        evaluate_base_model(client, dataset_path)
    except Exception:
        print("Evaluation failed due to API or dataset issue.")


if __name__ == "__main__":
    main()
