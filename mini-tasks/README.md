# Workshop Mini-Tasks & Assignments

This directory contains standalone, verifiable solutions for the preparatory mini-tasks assigned across the 4-week **Advanced AI Engineer** plan.

---

## Week 1: LLM APIs, Structured Outputs & Data Validation

### **Task 1: Verify Groq API Account & Python Connection**
- **File**: `week1/task1_verify_groq.py`
- **Objective**: Verify that the Groq API credentials are functioning properly and make a live inference call.
- **Run command**:
  ```bash
  python mini-tasks/week1/task1_verify_groq.py [optional_groq_api_key]
  ```

### **Task 2: Pydantic User Profile Schema Validation**
- **File**: `week1/task2_user_profile_pydantic.py`
- **Objective**: Implements a strict `UserProfile` schema validating `Name`, `Age`, `Email`, and Indian `PAN` (`[A-Z]{5}[0-9]{4}[A-Z]{1}`) with `@field_validator` and custom error handling for `ValidationError`.
- **Run command**:
  ```bash
  python mini-tasks/week1/task2_user_profile_pydantic.py
  ```

### **Task 3: Instructor Structured JSON Extraction**
- **File**: `week1/task3_instructor_structured_output.py`
- **Objective**: Leverages `instructor` with `groq` to extract structured data matching the Pydantic schema from raw unstructured text.
- **Run command**:
  ```bash
  python mini-tasks/week1/task3_instructor_structured_output.py [optional_groq_api_key]
  ```

---

## Week 3: Multi-turn Conversation Memory

### **Task 1: Stateless vs Stateful Architecture**
- **File**: `week3/task1_stateless_vs_stateful.py`
- **Objective**: Demonstrates how stateless LLM calls lose context and how a memory buffer re-injects conversation turns.
- **Run command**:
  ```bash
  python mini-tasks/week3/task1_stateless_vs_stateful.py
  ```

### **Task 2: Session IDs & Chat Isolation**
- **File**: `week3/task2_session_ids_isolation.py`
- **Objective**: Demonstrates generating unique UUID session IDs, storing isolated chat histories, and supporting a "New Chat" feature.
- **Run command**:
  ```bash
  python mini-tasks/week3/task2_session_ids_isolation.py
  ```

### **Task 3: Practice Sending Conversation History to Groq**
- **File**: `week3/task3_groq_conversation_history.py`
- **Objective**: Demonstrates maintaining multi-turn context (system, user, assistant messages) and resolving contextual follow-up questions with Groq.
- **Run command**:
  ```bash
  python mini-tasks/week3/task3_groq_conversation_history.py [optional_groq_api_key]
  ```

---

## Automated Verification Suite

Run all automated unit tests for the mini-tasks:
```bash
pytest mini-tasks/tests/test_mini_tasks.py -v
```

