from typing import Sequence

from fastapi import HTTPException, status

from app.models import User
from app.repositories import UserRepository


class UserService:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    def _get_or_404(self, user_id: int) -> User:
        user = self.users.get(user_id)
        if user is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Пользователь не найден")
        return user

    def list_users(self) -> Sequence[User]:
        return self.users.list_all()

    def set_banned(self, user_id: int, banned: bool) -> User:
        return self.users.set_banned(self._get_or_404(user_id), banned)

    def follow(self, current_user: User, target_id: int) -> None:
        if target_id == current_user.id:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Нельзя подписаться на себя")
        self._get_or_404(target_id)
        if self.users.is_following(current_user.id, target_id):
            raise HTTPException(status.HTTP_409_CONFLICT, "Вы уже подписаны")
        self.users.follow(current_user.id, target_id)

    def unfollow(self, current_user: User, target_id: int) -> None:
        if not self.users.is_following(current_user.id, target_id):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Подписка не найдена")
        self.users.unfollow(current_user.id, target_id)
