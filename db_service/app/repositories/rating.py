from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import PostRating


class RatingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, user_id: int, post_id: int) -> PostRating | None:
        return self.db.get(PostRating, (user_id, post_id))

    def list_by_post(self, post_id: int) -> Sequence[PostRating]:
        stmt = select(PostRating).where(PostRating.post_id == post_id).order_by(PostRating.user_id)
        return self.db.scalars(stmt).all()

    def save(self, user_id: int, post_id: int, score: int, review_text: str | None) -> PostRating:
        """Создаёт оценку или обновляет существующую (одна оценка на пару user/post)."""
        rating = self.get(user_id, post_id)
        if rating is None:
            rating = PostRating(user_id=user_id, post_id=post_id, score=score, review_text=review_text)
            self.db.add(rating)
        else:
            rating.score = score
            rating.review_text = review_text
        self.db.commit()
        self.db.refresh(rating)
        return rating

    def delete(self, rating: PostRating) -> None:
        self.db.delete(rating)
        self.db.commit()
