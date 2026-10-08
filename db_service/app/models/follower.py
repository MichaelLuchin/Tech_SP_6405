from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Follower(Base):
    __tablename__ = "follower"

    follower_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    followed_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )

    def __repr__(self) -> str:
        return f"<Follower(follower_id={self.follower_id}, followed_id={self.followed_id})>"