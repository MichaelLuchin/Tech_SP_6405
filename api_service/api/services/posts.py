from typing import Sequence

from fastapi import HTTPException, status

from app.models import Post, User
from app.repositories import PostRepository
from api.config import ADMIN_ROLE
from api.schemas import PostCreate, PostUpdate


class PostService:
    def __init__(self, posts: PostRepository) -> None:
        self.posts = posts

    def get(self, post_id: int) -> Post:
        post = self.posts.get(post_id)
        if post is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Пост не найден")
        return post

    def list_posts(self) -> Sequence[Post]:
        return self.posts.list_all()

    def feed(self, user: User) -> Sequence[Post]:
        return self.posts.list_feed(user.id)

    def create(self, user: User, data: PostCreate) -> Post:
        return self.posts.create(user.id, data.content)

    def update(self, user: User, post_id: int, data: PostUpdate) -> Post:
        post = self.get(post_id)
        if post.author_id != user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Можно редактировать только свои посты")
        return self.posts.update(post, data.content)

    def delete(self, user: User, post_id: int) -> None:
        post = self.get(post_id)
        if post.author_id != user.id and user.role.name != ADMIN_ROLE:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Можно удалять только свои посты")
        self.posts.delete(post)
