from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, joinedload

from app.models import Follower, Role, User, UserPassword


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, user_id: int) -> User | None:
        return self.db.get(User, user_id, options=[joinedload(User.role)])

    def get_by_username(self, username: str) -> User | None:
        stmt = (
            select(User)
            .options(joinedload(User.role), joinedload(User.password))
            .where(User.username == username)
        )
        return self.db.scalar(stmt)

    def list_all(self) -> Sequence[User]:
        stmt = select(User).options(joinedload(User.role)).order_by(User.id)
        return self.db.scalars(stmt).all()

    def get_or_create_role(self, name: str) -> Role:
        role = self.db.scalar(select(Role).where(Role.name == name))
        if role is None:
            role = Role(name=name)
            self.db.add(role)
            self.db.commit()
        return role

    def create(self, username: str, role_id: int, password_hash: str) -> User:
        user = User(
            username=username,
            role_id=role_id,
            password=UserPassword(password_hash=password_hash),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def set_banned(self, user: User, banned: bool) -> User:
        user.is_banned = banned
        self.db.commit()
        self.db.refresh(user)
        return user

    # --- подписки ---
    def is_following(self, follower_id: int, followed_id: int) -> bool:
        return self.db.get(Follower, (follower_id, followed_id)) is not None

    def follow(self, follower_id: int, followed_id: int) -> None:
        self.db.add(Follower(follower_id=follower_id, followed_id=followed_id))
        self.db.commit()

    def unfollow(self, follower_id: int, followed_id: int) -> None:
        self.db.execute(
            delete(Follower).where(
                Follower.follower_id == follower_id,
                Follower.followed_id == followed_id,
            )
        )
        self.db.commit()
