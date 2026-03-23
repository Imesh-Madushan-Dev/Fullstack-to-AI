import os
from dotenv import load_dotenv
from datetime import datetime
import google.genai as genai

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit()

# Create client
client = genai.Client(api_key=api_key)

# Message history (for context)
messages = []

# Helper function: Count tokens (rough estimate)
def count_tokens(text: str) -> int:
    """Rough token count: ~4 characters per token"""
    return len(text) // 4

# Helper function: Save chat log
def save_chat_log(messages: list):
    """Save conversation to a timestamped .txt file"""
    if not messages:
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_log_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=== Gemini Chat Log ===\n")
        f.write(f"Saved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        for msg in messages:
            role = "User" if msg['role'] == 'user' else 'Assistant'
            f.write(f"{role}:\n{msg['content']}\n\n")
    
    print(f"✓ Chat saved to: {filename}")

# Chat loop
print("Chat with Gemini! Type 'exit' to quit, '/clear' to reset.\n")

while True:
    user_input = input("You: ").strip()
    
    # Exit condition
    if user_input.lower() == "exit":
        print("\nGoodbye!")
        # Save chat log before exiting
        save_chat_log(messages)
        break
    
    # Clear conversation command
    if user_input.lower() == "/clear":
        messages = []
        print("✓ Conversation cleared.\n")
        continue
    
    # Skip empty input
    if not user_input:
        continue
    
    # Add user message to history
    messages.append({"role": "user", "content": user_input})
    
    # Build conversation text from history
    conversation = "\n".join(
        f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
        for m in messages
    )
    
    # Count tokens
    token_count = count_tokens(conversation)
    
    # Send to Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation
    )
    reply = response.text
    
    # Add AI response to history
    messages.append({"role": "assistant", "content": reply})
    
    # Print response with token count
    print(f"\nAI: {reply}\n")
    print(f"[Tokens used: ~{token_count}]\n")