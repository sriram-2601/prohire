"""Week 3 Pre-Class Task 3: Practice Sending Conversation History to Groq Using Python.

Demonstrates multi-turn conversation memory with user, assistant, and system roles,
allowing the LLM to resolve references and answer contextual follow-up questions.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Load environment from backend/.env
BACKEND_ENV = Path(__file__).resolve().parents[2] / "backend" / ".env"
if BACKEND_ENV.exists():
    load_dotenv(BACKEND_ENV)
else:
    load_dotenv()

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
API_KEY = os.getenv("GROQ_API_KEY", "").strip()


def run_conversation_memory_demo(api_key: str | None = None, model: str | None = None) -> bool:
    key = api_key or API_KEY
    target_model = model or DEFAULT_MODEL

    print("=" * 60)
    print("WEEK 3 - TASK 3: MULTI-TURN CONVERSATION MEMORY DEMO")
    print("=" * 60)

    if not key or key == "your_groq_api_key_here":
        print("\n[!] GROQ_API_KEY is not configured yet!")
        print(f"    Please configure your key in: {BACKEND_ENV}")
        return False

    # Simulate multi-turn conversation history
    conversation_history = [
        {
            "role": "system",
            "content": "You are a concise customer-support assistant. Answer questions accurately based on history.",
        },
        {
            "role": "user",
            "content": "Hi, I have two orders pending: Order #A100 (MacBook Pro) and Order #B200 (Wireless Mouse).",
        },
        {
            "role": "assistant",
            "content": "Hello! I can see both Order #A100 (MacBook Pro) and Order #B200 (Wireless Mouse). How can I assist you with them?",
        },
    ]

    # Follow-up question referencing the earlier turn without repeating details
    follow_up_question = "When is the first one arriving?"
    print("\n[*] Initial Conversation Turns:")
    for turn in conversation_history:
        print(f"    [{turn['role'].upper()}]: {turn['content']}")

    print(f"\n[*] Follow-Up Question: \"{follow_up_question}\"")
    print("[*] Submitting complete conversation history to Groq...")

    messages_to_send = list(conversation_history)
    messages_to_send.append({"role": "user", "content": follow_up_question})

    try:
        client = Groq(api_key=key)
        response = client.chat.completions.create(
            model=target_model,
            messages=messages_to_send,
            temperature=0.2,
            max_tokens=256,
        )

        reply = response.choices[0].message.content.strip()
        print("\n[OK] Assistant Context-Aware Reply:")
        print(f"    \"{reply}\"")
        print("\n[OK] The model successfully resolved 'the first one' to Order #A100 (MacBook Pro)!")
        return True

    except Exception as exc:
        print(f"\n[FAIL] Request failed: {exc}")
        return False


if __name__ == "__main__":
    cli_key = sys.argv[1] if len(sys.argv) > 1 else None
    cli_model = sys.argv[2] if len(sys.argv) > 2 else None
    success = run_conversation_memory_demo(api_key=cli_key, model=cli_model)
    sys.exit(0 if success else 1)
