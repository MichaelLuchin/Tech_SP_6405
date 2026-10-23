from typing import Sequence

from fastapi import HTTPException, status

from app.models import PostRating, User
from app.repositories import PostRepository, RatingRepository
from api.schemas import RatingSet


class RatingService:
    def __init__(self, ratings: RatingRepository, posts: PostRepository) -> None:
        self.ratings = ratings
        self.posts = posts

    def _get_post_or_404(self, post_id: int):
        post = self.posts.get(post_id)
        if post is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Пост не найден")
        return post

    def set_rating(self, user: User, post_id: int, data: RatingSet) -> PostRating:
        post = self._get_post_or_404(post_id)
        if post.author_id == user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Нельзя оценивать собственный пост")
        return self.ratings.save(user.id, post_id, data.score, data.review_text)

    def list_for_post(self, post_id: int) -> Sequence[PostRating]:
        self._get_post_or_404(post_id)
        return self.ratings.list_by_post(post_id)

    def delete(self, post_id: int, rating_user_id: int) -> None:
        rating = self.ratings.get(rating_user_id, post_id)
        if rating is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Оценка не найдена")
        self.ratings.delete(rating)
