from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Follower, Post


class PostRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, post_id: int) -> Post | None:
        return self.db.get(Post, post_id)

    def list_all(self) -> Sequence[Post]:
        return self.db.scalars(select(Post).order_by(Post.id.desc())).all()

    def list_feed(self, user_id: int) -> Sequence[Post]:
        """Посты авторов, на которых подписан пользователь."""
        stmt = (
            select(Post)
            .join(Follower, Follower.followed_id == Post.author_id)
            .where(Follower.follower_id == user_id)
            .order_by(Post.id.desc())
        )
        return self.db.scalars(stmt).all()

    def create(self, author_id: int, content: str) -> Post:
        post = Post(author_id=author_id, content=content)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def update(self, post: Post, content: str) -> Post:
        post.content = content
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete(self, post: Post) -> None:
        self.db.delete(post)
        self.db.commit()
