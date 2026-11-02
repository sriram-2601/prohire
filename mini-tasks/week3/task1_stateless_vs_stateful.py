"""Week 3 Pre-Class Task 1: Stateless vs Stateful Architecture in LLM Applications.

Demonstrates why HTTP APIs and LLMs are fundamentally stateless, and how
conversation memory layers convert stateless interactions into stateful sessions.
"""

def demonstrate_stateless():
    print("\n--- 1. STATELESS INTERACTION (Context is Lost) ---")
    # Turn 1: User introduces their name
    turn_1 = "My name is John Doe and my order ID is ORD-8899."
    print(f"User Request 1 : \"{turn_1}\"")
    print("Server Response : \"Nice to meet you John Doe, I have noted order ORD-8899.\"")

    # Turn 2: User asks a follow-up question in a stateless call
    turn_2 = "What is my order ID?"
    print(f"\nUser Request 2 : \"{turn_2}\" (Sent without previous messages)")
    print("Server Response : \"I am sorry, but you haven't mentioned your order ID yet. Please provide it.\"")
    print("-> Result: The server and model had no memory of Turn 1!")


def demonstrate_stateful():
    print("\n--- 2. STATEFUL INTERACTION (Managed with Memory Layer) ---")
    # In-memory history buffer
    chat_history = []

    # Turn 1
    turn_1 = "My name is John Doe and my order ID is ORD-8899."
    print(f"User Request 1 : \"{turn_1}\"")
    chat_history.append({"role": "user", "content": turn_1})
    bot_reply_1 = "Nice to meet you John Doe, I have noted order ORD-8899."
    chat_history.append({"role": "assistant", "content": bot_reply_1})
    print(f"Server Response : \"{bot_reply_1}\"")

    # Turn 2: Send previous turns along with the new question
    turn_2 = "What is my order ID?"
    print(f"\nUser Request 2 : \"{turn_2}\"")
    print(f"Payload sent to LLM with history ({len(chat_history)} previous turns):")
    for i, msg in enumerate(chat_history, start=1):
        print(f"  [{i}] {msg['role']}: {msg['content']}")

    bot_reply_2 = "Your order ID is ORD-8899."
    print(f"Server Response : \"{bot_reply_2}\"")
    print("-> Result: The assistant correctly answered using conversational history!")


def run_demo():
    print("=" * 65)
    print("WEEK 3 - TASK 1: STATELESS VS STATEFUL ARCHITECTURE DEMO")
    print("=" * 65)
    demonstrate_stateless()
    demonstrate_stateful()
    print("\nKey Architectural Takeaway:")
    print("1. LLMs and HTTP APIs are inherently stateless.")
    print("2. Memory must be managed on the application level (in-memory or DB).")
    print("3. Each query re-injects relevant prior conversation context.")
    print("\n[OK] Task 1 completed successfully!")


if __name__ == "__main__":
    run_demo()
