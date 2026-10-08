from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.follower import Follower

if TYPE_CHECKING:
    from app.models.role import Role
    from app.models.post import Post
    from app.models.rating import PostRating


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), nullable=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Связи
    role: Mapped["Role"] = relationship(back_populates="users")

    # 1:1 с паролем (uselist=False)
    password: Mapped[Optional["UserPassword"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False
    )

    # 1:N с постами
    posts: Mapped[List["Post"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )

    # 1:N с оценками постов
    ratings: Mapped[List["PostRating"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Self-referential N:M для подписок через таблицу follower
    following: Mapped[List["User"]] = relationship(
        "User",
        secondary=Follower.__table__,
        primaryjoin=id == Follower.follower_id,
        secondaryjoin=id == Follower.followed_id,
        back_populates="followers"
    )

    followers: Mapped[List["User"]] = relationship(
        "User",
        secondary=Follower.__table__,
        primaryjoin=id == Follower.followed_id,
        secondaryjoin=id == Follower.follower_id,
        back_populates="following"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username!r}, role_id={self.role_id}, is_banned={self.is_banned})>"


class UserPassword(Base):
    __tablename__ = "user_password"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    user: Mapped["User"] = relationship(back_populates="password")

    def __repr__(self) -> str:
        return f"<UserPassword(user_id={self.user_id})>"