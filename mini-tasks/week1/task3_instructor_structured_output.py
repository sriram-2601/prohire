"""Week 1 Mini Task 3: Generate Structured JSON Responses with Instructor + Groq + Pydantic.

Takes an unstructured natural language text and extracts a strictly typed Pydantic
schema via Instructor and Groq Cloud LLM.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import instructor
from groq import Groq
from pydantic import BaseModel, ConfigDict, Field

# Load backend/.env
BACKEND_ENV = Path(__file__).resolve().parents[2] / "backend" / ".env"
if BACKEND_ENV.exists():
    load_dotenv(BACKEND_ENV)
else:
    load_dotenv()

DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
API_KEY = os.getenv("GROQ_API_KEY", "").strip()


class ExtractedUserProfile(BaseModel):
    """Schema for extracting customer details from natural language text."""
    model_config = ConfigDict(extra="forbid")

    full_name: str = Field(description="Full legal name of the individual")
    age: int = Field(description="Age in years")
    email: str = Field(description="Email address")
    pan: str = Field(description="Indian Permanent Account Number (10 alphanumeric characters, 5 letters + 4 digits + 1 letter)")
    inquiry_summary: str = Field(description="A brief 1-sentence summary of what the user requested")


SAMPLE_TEXT = (
    "Hello team! My name is Priya Sharma. I am 29 years old. "
    "You can reach me at priya.sharma@example.in. "
    "For KYC verification, my Indian PAN card number is ABCDE5678G. "
    "Could you please confirm if my account activation is complete?"
)


def extract_structured_data(
    unstructured_text: str = SAMPLE_TEXT,
    api_key: str | None = None,
    model: str | None = None,
) -> ExtractedUserProfile | None:
    key = api_key or API_KEY
    target_model = model or DEFAULT_MODEL

    print("=" * 60)
    print("WEEK 1 - TASK 3: INSTRUCTOR STRUCTURED JSON GENERATION")
    print("=" * 60)

    if not key or key == "your_groq_api_key_here":
        print("\n[!] GROQ_API_KEY is not configured yet!")
        print(f"    Please configure your key in: {BACKEND_ENV}")
        print("    Or pass it directly: python task3_instructor_structured_output.py gsk_your_key")
        return None

    print("\n[*] Unstructured Input Text:")
    print(f"    \"{unstructured_text}\"")
    print(f"\n[*] Calling Groq ({target_model}) via Instructor client...")

    try:
        groq_client = Groq(api_key=key)
        client = instructor.from_groq(groq_client, mode=instructor.Mode.JSON)

        profile: ExtractedUserProfile = client.chat.completions.create(
            model=target_model,
            response_model=ExtractedUserProfile,
            temperature=0,
            max_retries=2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract the user profile and inquiry summary from the provided input text. "
                        "Adhere strictly to the requested schema. Return valid JSON only."
                    ),
                },
                {"role": "user", "content": unstructured_text},
            ],
        )

        print("\n[OK] Successfully Generated & Validated Structured Output!")
        print("-" * 50)
        print(f"Full Name : {profile.full_name}")
        print(f"Age       : {profile.age}")
        print(f"Email     : {profile.email}")
        print(f"PAN       : {profile.pan}")
        print(f"Summary   : {profile.inquiry_summary}")
        print("-" * 50)
        print("\nStructured JSON Dump:")
        print(profile.model_dump_json(indent=2))
        print("\n[OK] Task 3 completed successfully!")
        return profile

    except Exception as exc:
        print(f"\n[FAIL] Failed during extraction: {exc}")
        return None


if __name__ == "__main__":
    cli_key = sys.argv[1] if len(sys.argv) > 1 else None
    cli_model = sys.argv[2] if len(sys.argv) > 2 else None
    result = extract_structured_data(api_key=cli_key, model=cli_model)
    sys.exit(0 if result else 1)
