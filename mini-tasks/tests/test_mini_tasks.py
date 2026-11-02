import pytest
from pydantic import ValidationError

import sys
from pathlib import Path
import pytest
from pydantic import ValidationError

MINI_TASKS_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MINI_TASKS_DIR))

from week1.task2_user_profile_pydantic import UserProfile
from week3.task2_session_ids_isolation import SessionMemoryStore


def test_user_profile_accepts_valid_pan_and_details():
    profile = UserProfile(
        name="Sunil Gavaskar",
        age=35,
        email="sunil.g@example.com",
        pan="ABCDE1234F",
    )
    assert profile.name == "Sunil Gavaskar"
    assert profile.age == 35
    assert profile.email == "sunil.g@example.com"
    assert profile.pan == "ABCDE1234F"


def test_user_profile_rejects_underage():
    with pytest.raises(ValidationError) as exc:
        UserProfile(
            name="Ravi Kumar",
            age=16,
            email="ravi@example.com",
            pan="ABCDE1234F",
        )
    assert "greater than or equal to 18" in str(exc.value)


def test_user_profile_rejects_invalid_pan_format():
    with pytest.raises(ValidationError) as exc:
        UserProfile(
            name="Ravi Kumar",
            age=25,
            email="ravi@example.com",
            pan="12345ABCDE",  # invalid PAN structure
        )
    assert "Invalid PAN format" in str(exc.value)


def test_user_profile_rejects_invalid_email():
    with pytest.raises(ValidationError) as exc:
        UserProfile(
            name="Ravi Kumar",
            age=25,
            email="not_an_email_address",
            pan="ABCDE1234F",
        )
    assert "not a valid email address" in str(exc.value)


def test_session_isolation():
    store = SessionMemoryStore()
    s1 = store.create_session()
    s2 = store.create_session()

    store.add_message(s1, "user", "Message for S1")
    store.add_message(s2, "user", "Message for S2")

    h1 = store.get_history(s1)
    h2 = store.get_history(s2)

    assert len(h1) == 1
    assert len(h2) == 1
    assert h1[0]["content"] == "Message for S1"
    assert h2[0]["content"] == "Message for S2"
