from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.db import get_db
from app.models import User

password_hash = PasswordHash.recommended()
bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


def create_access_token(user: User) -> str:
    settings = get_settings()
    payload = {"sub": str(user.id), "company_id": user.company_id, "sv": user.session_version, "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def create_two_factor_challenge(user: User) -> str:
    settings = get_settings()
    payload = {
        "sub": str(user.id),
        "purpose": "two_factor",
        "sv": user.session_version,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def read_two_factor_challenge(token: str) -> tuple[int, int]:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        if payload.get("purpose") != "two_factor":
            raise ValueError
        return int(payload["sub"]), int(payload["sv"])
    except (jwt.PyJWTError, KeyError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Kod weryfikacyjny wygasł. Zaloguj się ponownie.") from exc


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    settings = get_settings()
    token = credentials.credentials if credentials and credentials.credentials not in {"null", "undefined"} else request.cookies.get("buildsmart_session")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if payload.get("sv") != user.session_version:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return user


def require_roles(*allowed_roles: str):
    """Ogranicza czynności administracyjne do właściciela lub administratora."""
    def role_guard(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Nie masz uprawnień do tej czynności.")
        return user
    return role_guard
