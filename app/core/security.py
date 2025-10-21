from datetime import datetime, timedelta, timezone
import jwt
from argon2 import PasswordHasher
from typing import Any, Dict
from .config import settings

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        ph.verify(hashed, password)
        return True
    except Exception:
        return False

def create_jwt(payload: Dict[str, Any], expires_delta: timedelta) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    to_encode.update({"iat": int(now.timestamp()), "exp": int((now + expires_delta).timestamp())})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_alg)

def create_access_token(sub: str) -> str:
    return create_jwt({"sub": sub, "typ": "access"}, timedelta(minutes=settings.access_token_expire_minutes))

def create_refresh_token(sub: str) -> str:
    return create_jwt({"sub": sub, "typ": "refresh"}, timedelta(days=settings.refresh_token_expire_days))
