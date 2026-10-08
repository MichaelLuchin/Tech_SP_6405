from typing import TYPE_CHECKING, List
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.rating import PostRating

class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Связи
    author: Mapped["User"] = relationship(back_populates="posts")
    ratings: Mapped[List["PostRating"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, author_id={self.author_id})>"