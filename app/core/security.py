from datetime import UTC, datetime, timedelta
from typing import Any
from passlib.context import CryptContext
import jwt
from app.core.config import Settings
from app.core.exceptions import UnauthorizedError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(pwd: str) -> str:
    return pwd_context.hash(pwd)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(*, subject: str, settings: Settings) -> str:
    """Создаёт access token"""

    expire_at = datetime.now(UTC) + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES,
    )
    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire_at,
        "type": "access",
    }
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str, settings: Settings) -> dict[str, Any]:
    """Декодирует access token"""

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError as exc:
        raise UnauthorizedError("Invalid access token.") from exc

    if payload.get("type") != "access":
        raise UnauthorizedError("Unsupported token type.")

    return payload
