"""Week 1 Mini Task 2: Pydantic User Profile Schema with Name, Age, Email, and PAN Validation.

Tests validation rules with valid and invalid data, catching and displaying ValidationError.
"""
import re
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


PAN_REGEX = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


class UserProfile(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(..., min_length=2, max_length=100, description="Full name of the user")
    age: int = Field(..., ge=18, le=120, description="User age (must be between 18 and 120)")
    email: str = Field(..., min_length=5, max_length=255, description="Valid email address")
    pan: str = Field(..., description="Indian Permanent Account Number (e.g. ABCDE1234F)")

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = " ".join(value.split())
        if not all(c.isalpha() or c.isspace() or c in ".-'" for c in cleaned):
            raise ValueError("Name can only contain alphabets, spaces, dots, hyphens, and apostrophes.")
        return cleaned

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.lower()
        if not EMAIL_REGEX.match(value):
            raise ValueError(f"'{value}' is not a valid email address.")
        return value

    @field_validator("pan")
    @classmethod
    def validate_pan(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not PAN_REGEX.match(normalized):
            raise ValueError(
                f"Invalid PAN format '{value}'. PAN must consist of 5 uppercase letters, "
                f"4 digits, and 1 uppercase letter (e.g., ABCDE1234F)."
            )
        return normalized


def run_demo():
    print("=" * 60)
    print("WEEK 1 - TASK 2: PYDANTIC USER PROFILE VALIDATION DEMO")
    print("=" * 60)

    # 1. Valid Profile
    print("\n[+] 1. Testing with VALID data:")
    valid_data = {
        "name": "Arun Kumar",
        "age": 28,
        "email": "arun.kumar@example.com",
        "pan": "ABCDE1234F",
    }
    try:
        user = UserProfile(**valid_data)
        print("    Success! User profile parsed & validated:")
        print(f"    Name  : {user.name}")
        print(f"    Age   : {user.age}")
        print(f"    Email : {user.email}")
        print(f"    PAN   : {user.pan}")
    except ValidationError as e:
        print(f"    Unexpected validation error: {e}")

    # 2. Invalid Profile - Bad Age & Bad PAN
    print("\n[-] 2. Testing with INVALID data (Age < 18, Malformed PAN, Invalid Email):")
    invalid_data = {
        "name": "Youngster123",
        "age": 15,
        "email": "not-an-email",
        "pan": "INVALID_PAN_123",
    }
    try:
        UserProfile(**invalid_data)
        print("    Error: Expected validation failure, but succeeded!")
    except ValidationError as exc:
        print("    Caught expected ValidationError as designed:")
        for idx, error in enumerate(exc.errors(), start=1):
            field = " -> ".join(str(loc) for loc in error["loc"])
            msg = error["msg"]
            print(f"      {idx}. Field '{field}': {msg}")

    # 3. Invalid Profile - Extra unexpected fields (ConfigDict extra='forbid')
    print("\n[-] 3. Testing with forbidden extra field:")
    extra_data = {
        "name": "Jane Doe",
        "age": 30,
        "email": "jane@example.com",
        "pan": "BNZPK9876Q",
        "is_admin": True,
    }
    try:
        UserProfile(**extra_data)
    except ValidationError as exc:
        print("    Caught expected ValidationError for forbidden extra field:")
        for idx, error in enumerate(exc.errors(), start=1):
            print(f"      {idx}. Field '{error['loc'][0]}': {error['msg']}")

    print("\n[OK] Task 2 completed successfully!")


if __name__ == "__main__":
    run_demo()
