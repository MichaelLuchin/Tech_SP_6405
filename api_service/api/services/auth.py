from fastapi import HTTPException, status

from app.models import User
from app.passwords import hash_password, verify_password
from app.repositories import UserRepository
from api.config import DEFAULT_ROLE
from api.schemas import Token, UserCreate
from api.security import create_access_token


class AuthService:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    def register(self, data: UserCreate) -> User:
        if self.users.get_by_username(data.username):
            raise HTTPException(status.HTTP_409_CONFLICT, "Имя пользователя уже занято")
        role = self.users.get_or_create_role(DEFAULT_ROLE)
        return self.users.create(data.username, role.id, hash_password(data.password))

    def login(self, username: str, password: str) -> Token:
        user = self.users.get_by_username(username)
        if user is None or user.password is None or not verify_password(password, user.password.password_hash):
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Неверное имя пользователя или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if user.is_banned:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Аккаунт заблокирован")
        return Token(access_token=create_access_token(user.id))
