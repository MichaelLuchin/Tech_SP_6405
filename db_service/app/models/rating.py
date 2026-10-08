from typing import TYPE_CHECKING, Optional
from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.post import Post

class PostRating(Base):
    __tablename__ = "post_rating"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("post.id", ondelete="CASCADE"), primary_key=True
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    review_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Связи
    user: Mapped["User"] = relationship(back_populates="ratings")
    post: Mapped["Post"] = relationship(back_populates="ratings")

    def __repr__(self) -> str:
        return f"<PostRating(user_id={self.user_id}, post_id={self.post_id}, score={self.score})>"