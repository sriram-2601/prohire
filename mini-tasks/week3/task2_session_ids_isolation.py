"""Week 3 Pre-Class Task 2: Session IDs and Conversation Isolation.

Demonstrates creating unique session identifiers (UUIDv4) to guarantee
isolation between parallel conversations in an in-memory session store.
"""
from uuid import uuid4
from typing import Dict, List


class SessionMemoryStore:
    def __init__(self):
        # Maps session_id (str) -> list of message dicts
        self._sessions: Dict[str, List[dict]] = {}

    def create_session(self) -> str:
        session_id = str(uuid4())
        self._sessions[session_id] = []
        return session_id

    def add_message(self, session_id: str, role: str, content: str) -> None:
        if session_id not in self._sessions:
            raise KeyError(f"Session {session_id} does not exist.")
        self._sessions[session_id].append({"role": role, "content": content})

    def get_history(self, session_id: str) -> List[dict]:
        return list(self._sessions.get(session_id, []))

    def reset_session(self, session_id: str) -> str:
        """Simulates 'New Chat': creates and returns a brand new session ID."""
        return self.create_session()


def run_demo():
    print("=" * 65)
    print("WEEK 3 - TASK 2: SESSION ID & CHAT ISOLATION DEMO")
    print("=" * 65)

    store = SessionMemoryStore()

    # User Alice starts a session
    alice_session = store.create_session()
    print(f"\n[+] Created Session for Alice : {alice_session}")
    store.add_message(alice_session, "user", "I need help with my Python script.")
    store.add_message(alice_session, "assistant", "Sure, what Python issue are you facing?")

    # User Bob starts a session
    bob_session = store.create_session()
    print(f"[+] Created Session for Bob   : {bob_session}")
    store.add_message(bob_session, "user", "Can you track my flight to Mumbai?")
    store.add_message(bob_session, "assistant", "Please provide your flight number.")

    print("\n--- Verifying Strict Session Isolation ---")
    alice_history = store.get_history(alice_session)
    bob_history = store.get_history(bob_session)

    print(f"Alice's chat turn count: {len(alice_history)}")
    for turn in alice_history:
        print(f"  Alice [{turn['role']}]: {turn['content']}")

    print(f"\nBob's chat turn count: {len(bob_history)}")
    for turn in bob_history:
        print(f"  Bob [{turn['role']}]: {turn['content']}")

    # Verify that Alice's keywords never leak into Bob's session
    assert all("flight" not in msg["content"] for msg in alice_history)
    assert all("Python" not in msg["content"] for msg in bob_history)
    print("\n[OK] Confirmed: No data cross-talk between isolated sessions!")

    # Simulate 'New Chat'
    new_session = store.reset_session(alice_session)
    print(f"\n[+] User Alice clicks 'New Chat' -> New Session ID generated: {new_session}")
    print(f"    New session history count: {len(store.get_history(new_session))} (Clean state)")

    print("\n[OK] Task 2 completed successfully!")


if __name__ == "__main__":
    run_demo()

