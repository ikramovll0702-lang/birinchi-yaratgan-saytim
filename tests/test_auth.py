import pytest
from app.auth import hash_password, verify_password, sign_session_token, verify_session_token

def test_password_hashing():
    raw = "maxfiy_parol_2026"
    hashed = hash_password(raw)
    assert hashed != raw
    assert ":" in hashed
    assert verify_password(raw, hashed) is True
    assert verify_password("noto'g'ri_parol", hashed) is False

def test_session_token():
    user_id = 42
    token = sign_session_token(user_id)
    assert token is not None
    verified_id = verify_session_token(token)
    assert verified_id == user_id

def test_invalid_session_token():
    assert verify_session_token("") is None
    assert verify_session_token("invalid_token_string") is None
    assert verify_session_token("42:12345678:fakesignature") is None

