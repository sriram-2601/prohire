"""Week 1 Concept: Type Enforcement vs. Regex Parsing for LLM Outputs.

Demonstrates why regex parsing breaks when LLMs produce non-deterministic formatting,
and how Pydantic v2 type enforcement guarantees structured, reliable data ingestion.
"""
import json
import re
from pydantic import BaseModel, ConfigDict, Field, ValidationError


# Sample realistic non-deterministic LLM outputs for the same query:
# "Extract customer support ticket: Category: Billing, Severity: High, Order ID: 44921, Refund: True"
LLM_OUTPUT_CASES = [
    # Case 1: Standard JSON
    '{"category": "Billing", "severity": "High", "order_id": 44921, "refund_requested": true}',

    # Case 2: Markdown wrapped with backticks and comments
    '```json\n{\n  "category": "Billing",\n  "severity": "HIGH",\n  "order_id": "44921",\n  "refund_requested": "true"\n}\n```',

    # Case 3: Reordered keys, extra whitespace, stringified numbers
    '{\n  "refund_requested": true,\n  "category": "Billing",\n  "order_id": "ORD-44921",\n  "severity": "High"\n}',

    # Case 4: Invalid/Hallucinated severity
    '{"category": "Billing", "severity": "SuperCritical-Urgent!", "order_id": 44921, "refund_requested": false}',
]


# Regex approach: fragile pattern matching
def regex_parser(raw_text: str) -> dict | None:
    category_match = re.search(r'"category"\s*:\s*"([^"]+)"', raw_text)
    severity_match = re.search(r'"severity"\s*:\s*"([^"]+)"', raw_text)
    order_id_match = re.search(r'"order_id"\s*:\s*(\d+)', raw_text)
    refund_match = re.search(r'"refund_requested"\s*:\s*(true|false)', raw_text, re.IGNORECASE)

    if not (category_match and severity_match and order_id_match and refund_match):
        return None  # Failed regex match

    return {
        "category": category_match.group(1),
        "severity": severity_match.group(1),
        "order_id": int(order_id_match.group(1)),
        "refund_requested": refund_match.group(1).lower() == "true",
    }


# Pydantic v2 Approach: strict type coercion, validation, and normalization
class SupportTicketSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    category: str
    severity: str
    order_id: int
    refund_requested: bool

    @classmethod
    def from_llm_output(cls, raw_text: str) -> "SupportTicketSchema":
        cleaned = raw_text.strip()
        # Strip markdown fences if present
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
        data = json.loads(cleaned)

        # Handle stringified order IDs like 'ORD-44921' or '44921'
        if isinstance(data.get("order_id"), str):
            digits = "".join(c for c in data["order_id"] if c.isdigit())
            data["order_id"] = int(digits) if digits else 0

        # Enforce valid severity levels
        allowed_severities = {"low", "medium", "high", "critical"}
        sev = str(data.get("severity", "")).lower()
        if sev not in allowed_severities:
            raise ValueError(f"Invalid severity '{data.get('severity')}'. Must be one of {allowed_severities}")
        data["severity"] = sev

        # Handle string booleans like "true"
        if isinstance(data.get("refund_requested"), str):
            data["refund_requested"] = data["refund_requested"].lower() in ("true", "1", "yes")

        return cls(**data)


def run_comparison():
    print("=" * 68)
    print("WEEK 1: REGEX PARSING VS. PYDANTIC TYPE ENFORCEMENT COMPARISON")
    print("=" * 68)

    for idx, raw in enumerate(LLM_OUTPUT_CASES, start=1):
        print(f"\n[Case {idx}] Raw LLM Output:\n{raw[:70]}...")

        # Test Regex
        reg_result = regex_parser(raw)
        if reg_result:
            print(f"  Regex Parser    : [SUCCESS] -> {reg_result}")
        else:
            print("  Regex Parser    : [FAILED] -> Unable to match non-deterministic pattern!")

        # Test Pydantic
        try:
            pyd_result = SupportTicketSchema.from_llm_output(raw)
            print(f"  Pydantic Parser : [SUCCESS] -> category='{pyd_result.category}', "
                  f"severity='{pyd_result.severity}', order_id={pyd_result.order_id}, "
                  f"refund={pyd_result.refund_requested}")
        except (ValueError, ValidationError, json.JSONDecodeError) as exc:
            print(f"  Pydantic Parser : [CAUGHT INVALID DATA] -> {exc}")

    print("\n" + "=" * 68)
    print("KEY LESSON:")
    print("Regex assumes deterministic syntax. LLMs vary whitespace, quotes, formatting,")
    print("and types. Pydantic v2 + Instructor provides true resilience for enterprise ingestion.")
    print("=" * 68)


if __name__ == "__main__":
    run_comparison()
