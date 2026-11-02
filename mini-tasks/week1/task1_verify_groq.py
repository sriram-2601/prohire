"""Week 1 Mini Task 1: Verify Groq API Account and Configuration.

Connects to the Groq Cloud API, verifies credentials, and tests basic LLM completion.
"""
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Load environment from backend/.env or current working directory
BACKEND_ENV = Path(__file__).resolve().parents[2] / "backend" / ".env"
if BACKEND_ENV.exists():
    load_dotenv(BACKEND_ENV)
else:
    load_dotenv()

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
API_KEY = os.getenv("GROQ_API_KEY", "").strip()


def verify_groq_connection(api_key: str | None = None, model: str | None = None) -> bool:
    key = api_key or API_KEY
    target_model = model or DEFAULT_MODEL

    print("=" * 60)
    print("WEEK 1 - TASK 1: GROQ API VERIFICATION")
    print("=" * 60)

    if not key or key == "your_groq_api_key_here":
        print("\n[!] GROQ_API_KEY is not configured yet!")
        print("    1. Sign up for free at https://console.groq.com/keys")
        print("    2. Copy your API key (starts with 'gsk_')")
        print(f"    3. Paste it into: {BACKEND_ENV}")
        print("       GROQ_API_KEY=gsk_your_real_key_here")
        print("\n    Or pass it directly when running this script:")
        print("       python task1_verify_groq.py gsk_your_key_here")
        return False

    masked_key = key[:6] + "..." + key[-4:] if len(key) > 10 else "***"
    print(f"\n[*] Configured Key : {masked_key}")
    print(f"[*] Target Model   : {target_model}")
    print("[*] Sending test prompt to Groq API...")

    start_time = time.time()
    try:
        client = Groq(api_key=key)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a verification assistant. Respond with exact, concise answers.",
                },
                {
                    "role": "user",
                    "content": "Confirm that the connection is active by replying: 'Groq API connection verified successfully!'",
                },
            ],
            model=target_model,
            max_tokens=64,
            temperature=0.1,
        )
        elapsed = time.time() - start_time
        reply = chat_completion.choices[0].message.content.strip()
        usage = chat_completion.usage

        print("\n[OK] Groq API Response Received!")
        print(f"    Response : \"{reply}\"")
        print(f"    Latency  : {elapsed:.2f} seconds")
        if usage:
            print(f"    Tokens   : prompt={usage.prompt_tokens}, completion={usage.completion_tokens}, total={usage.total_tokens}")
        print("\n[OK] Task 1 completed successfully!")
        return True

    except Exception as exc:
        print(f"\n[FAIL] Failed to communicate with Groq: {exc}")
        print("Please check your API key, internet connection, and selected model.")
        return False


if __name__ == "__main__":
    cli_key = sys.argv[1] if len(sys.argv) > 1 else None
    cli_model = sys.argv[2] if len(sys.argv) > 2 else None
    success = verify_groq_connection(api_key=cli_key, model=cli_model)
    sys.exit(0 if success else 1)
