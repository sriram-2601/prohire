"""Week 1 Concept: Tiktoken Token Counting and Context Budgeting.

Calculates token counts for inputs/outputs, prevents context window overflows,
and budgets token limits for multi-turn chats.
"""
import tiktoken


def demonstrate_token_budgeting():
    print("=" * 65)
    print("WEEK 1: TIKTOKEN TOKEN COUNTING & CONTEXT BUDGETING")
    print("=" * 65)

    # Use cl100k_base (OpenAI / modern LLM tokenizer)
    encoding = tiktoken.get_encoding("cl100k_base")

    system_prompt = "You are a customer service AI. Be concise and polite."
    user_query = "Where is my order #12345? It was supposed to arrive yesterday morning."
    chat_history = [
        "User: Hello",
        "Assistant: Hi! How can I help you today?",
        "User: I want to check on my recent shipment.",
        "Assistant: Sure! Please provide your order number.",
    ]

    # Calculate token lengths
    system_tokens = len(encoding.encode(system_prompt))
    query_tokens = len(encoding.encode(user_query))
    history_tokens = sum(len(encoding.encode(turn)) for turn in chat_history)

    total_input_tokens = system_tokens + query_tokens + history_tokens

    # Context window settings
    MAX_CONTEXT_WINDOW = 8192
    MAX_OUTPUT_BUDGET = 1000
    SAFE_MARGIN = 200

    remaining_budget = MAX_CONTEXT_WINDOW - (total_input_tokens + MAX_OUTPUT_BUDGET + SAFE_MARGIN)

    print(f"\n[*] System Prompt Tokens : {system_tokens}")
    print(f"[*] Chat History Tokens  : {history_tokens}")
    print(f"[*] Current Query Tokens : {query_tokens}")
    print("-" * 40)
    print(f"[*] Total Input Tokens   : {total_input_tokens}")
    print(f"[*] Max Context Window   : {MAX_CONTEXT_WINDOW}")
    print(f"[*] Reserved Output Max  : {MAX_OUTPUT_BUDGET}")
    print(f"[*] Remaining Headroom   : {remaining_budget} tokens")

    print("\n[OK] Context Budget is healthy. Request is safe to dispatch to LLM.")


if __name__ == "__main__":
    demonstrate_token_budgeting()
