"""Week 2 Task: Dynamic Prompt Templating & Intent-Based Response Generation.

Demonstrates the Week 2 end-to-end workflow:
User Question -> Intent Detection -> Dynamic Prompt Template -> Markdown Response
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

# Load backend/.env
BACKEND_ENV = Path(__file__).resolve().parents[2] / "backend" / ".env"
if BACKEND_ENV.exists():
    load_dotenv(BACKEND_ENV)
else:
    load_dotenv()

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
API_KEY = os.getenv("GROQ_API_KEY", "").strip()


PROMPT_TEMPLATES = {
    "order_tracking": (
        "You are an e-commerce logistics specialist. "
        "The customer is asking about their order status. "
        "Acknowledge the order, explain estimated shipping timelines, and provide guidance in Markdown."
    ),
    "payment_issue": (
        "You are a billing & payments specialist. "
        "The customer is experiencing a transaction, refund, or billing problem. "
        "Be empathetic, explain the 3-5 business day refund cycle, and present steps in Markdown."
    ),
    "general_question": (
        "You are a helpful customer support assistant. Answer the user query clearly in Markdown."
    ),
}


def generate_intent_based_response(
    intent: str,
    user_message: str,
    api_key: str | None = None,
    model: str | None = None,
) -> str:
    key = api_key or API_KEY
    target_model = model or DEFAULT_MODEL

    if not key or key == "your_groq_api_key_here":
        raise RuntimeError("GROQ_API_KEY not configured.")

    system_instruction = PROMPT_TEMPLATES.get(intent, PROMPT_TEMPLATES["general_question"])

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_message},
    ]

    client = Groq(api_key=key)
    completion = client.chat.completions.create(
        model=target_model,
        messages=messages,
        temperature=0.3,
        max_tokens=500,
    )
    return completion.choices[0].message.content.strip()


def run_demo():
    print("=" * 65)
    print("WEEK 2: DYNAMIC PROMPT TEMPLATING & RESPONSE GENERATION")
    print("=" * 65)

    test_queries = [
        ("order_tracking", "I ordered a wireless headphone 3 days ago. When will it arrive?"),
        ("payment_issue", "I was charged twice for transaction #TXN99482. Please help with refund!"),
    ]

    for intent, query in test_queries:
        print(f"\n[+] Detected Intent : {intent}")
        print(f"[*] User Message    : \"{query}\"")
        print("[*] Generating dynamic Markdown response...")
        try:
            markdown_reply = generate_intent_based_response(intent, query)
            safe_reply = markdown_reply.encode("ascii", errors="replace").decode("ascii")
            print("\n--- Assistant Markdown Reply ---")
            print(safe_reply)
            print("-" * 50)
        except Exception as e:
            print(f"[FAIL] Error generating response: {e}")

    print("\n[OK] Week 2 response generation workflow completed successfully!")


if __name__ == "__main__":
    run_demo()
