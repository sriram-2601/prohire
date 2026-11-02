# Workshop Mini-Tasks & Assignments

This directory contains standalone, verifiable solutions and demonstrations for all tasks and key concepts across the 4-week **Advanced AI Engineer** plan.

---

## Week 1: LLM APIs, Structured Outputs & Data Validation

### **Task 1: Verify Groq API Account & Connection**
- **File**: `week1/task1_verify_groq.py`
- **Objective**: Verifies live connection to Groq Cloud API, validates latency, and counts tokens.
- **Run command**:
  ```bash
  python mini-tasks/week1/task1_verify_groq.py [optional_groq_api_key]
  ```

### **Task 2: Pydantic User Profile Schema Validation**
- **File**: `week1/task2_user_profile_pydantic.py`
- **Objective**: Implements strict `UserProfile` schema validating `Name`, `Age`, `Email`, and Indian `PAN` (`[A-Z]{5}[0-9]{4}[A-Z]{1}`) with `@field_validator` and custom `ValidationError` handling.
- **Run command**:
  ```bash
  python mini-tasks/week1/task2_user_profile_pydantic.py
  ```

### **Task 3: Instructor Structured JSON Extraction**
- **File**: `week1/task3_instructor_structured_output.py`
- **Objective**: Uses `instructor` with `groq` to extract structured JSON matching the Pydantic schema from unstructured text.
- **Run command**:
  ```bash
  python mini-tasks/week1/task3_instructor_structured_output.py [optional_groq_api_key]
  ```

### **Concept Demo: Type Enforcement vs. Regex Parsing**
- **File**: `week1/type_enforcement_vs_regex.py`
- **Objective**: Demonstrates why regex fails on non-deterministic LLM output variations and how Pydantic guarantees clean ingestion.
- **Run command**:
  ```bash
  python mini-tasks/week1/type_enforcement_vs_regex.py
  ```

### **Concept Demo: Tiktoken Token Counting & Context Budgeting**
- **File**: `week1/tiktoken_context_budgeting.py`
- **Objective**: Calculates prompt and completion token counts and budgets context windows to avoid token overflows.
- **Run command**:
  ```bash
  python mini-tasks/week1/tiktoken_context_budgeting.py
  ```

---

## Week 2: LLM Integration & Response Generation

### **Task: Dynamic Prompt Templating & Intent-Based Response Pipeline**
- **File**: `week2/task1_prompt_and_intent_workflow.py`
- **Objective**: Connects user input to intent-specific prompt templates and generates rich Markdown responses with tables and action plans.
- **Run command**:
  ```bash
  python mini-tasks/week2/task1_prompt_and_intent_workflow.py
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
  python mini-tasks/week3/task3_groq_conversation_history.py
  ```

---

## Week 4: Production Deployment & Testing

### **Task 5: Production Verification Suite**
- **File**: `week4/task5_production_testing.py`
- **Objective**: Automated test suite that validates `/health`, CORS, secret protection, `/api/analyze`, streaming, database persistence, and malformed input rejection on any live URL (local or Render).
- **Run command**:
  ```bash
  python mini-tasks/week4/task5_production_testing.py [optional_backend_url]
  ```

---

## Automated Test Suite

Run all automated unit tests for the mini-tasks:
```bash
pytest mini-tasks/tests/test_mini_tasks.py -v
```
