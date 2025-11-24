import asyncio

import pytest
from fastapi import HTTPException

from app.auth import jwt as auth_jwt
from app.auth.jwt import get_password_hash, verify_password, create_token, decode_token
from app.schemas.token import TokenType


async def _fake_not_blacklisted(jti: str):
    return False


def test_password_hash_and_verify():
    password = "SecurePass123!"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpass", hashed)


def test_create_and_decode_token(monkeypatch):
    # prevent calling real redis in decode_token
    monkeypatch.setattr("app.auth.redis.is_blacklisted", _fake_not_blacklisted)

    token = create_token("user123", TokenType.ACCESS)
    payload = asyncio.run(decode_token(token, TokenType.ACCESS, verify_exp=False))

    assert payload["sub"] == "user123"
    assert payload["type"] == TokenType.ACCESS.value
    assert "jti" in payload


def test_decode_invalid_token_type_raises(monkeypatch):
    monkeypatch.setattr("app.auth.redis.is_blacklisted", _fake_not_blacklisted)

    token = create_token("user123", TokenType.ACCESS)

    with pytest.raises(HTTPException):
        asyncio.run(decode_token(token, TokenType.REFRESH, verify_exp=False))
