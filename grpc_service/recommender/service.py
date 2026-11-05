from app.models import Post
from app.repositories import PostRepository, RatingRepository
from recommender.config import AUTHOR_BONUS, LIKE_THRESHOLD


class RecommendationService:
    """Рекомендует посты по истории оценок пользователя."""

    def __init__(self, posts: PostRepository, ratings: RatingRepository) -> None:
        self.posts = posts
        self.ratings = ratings

    def recommend(self, user_id: int, limit: int) -> list[tuple[Post, float]]:
        my_ratings = self.ratings.list_by_user(user_id)
        rated_ids = {r.post_id for r in my_ratings}
        liked_authors = {r.post.author_id for r in my_ratings if r.score >= LIKE_THRESHOLD}

        scored = []
        for post in self.posts.list_all():
            if post.author_id == user_id or post.id in rated_ids or post.author.is_banned:
                continue
            scores = [r.score for r in post.ratings]
            average = sum(scores) / len(scores) if scores else 0.0
            bonus = AUTHOR_BONUS if post.author_id in liked_authors else 0.0
            scored.append((post, average + bonus))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:limit]
