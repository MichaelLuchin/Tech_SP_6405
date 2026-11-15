import jwt

from notifier.config import ALGORITHM, SECRET_KEY


def decode_access_token(token: str) -> int:
    """Возвращает id пользователя. Бросает jwt.InvalidTokenError, если токен недействителен."""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    try:
        return int(payload["sub"])
    except (KeyError, ValueError):
        raise jwt.InvalidTokenError("Некорректное содержимое токена")
