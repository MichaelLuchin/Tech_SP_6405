from datetime import datetime, timedelta, timezone

import jwt

from api.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> int:
    """Возвращает id пользователя. Бросает jwt.InvalidTokenError, если токен недействителен."""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    try:
        return int(payload["sub"])
    except (KeyError, ValueError):
        raise jwt.InvalidTokenError("Некорректное содержимое токена")
