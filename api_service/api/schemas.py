"""DTO (Pydantic) для HTTP-запросов и ответов. Отделены от ORM-моделей."""
from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# --- auth / users ---
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=128)


class RoleRead(ORMModel):
    id: int
    name: str


class UserRead(ORMModel):
    id: int
    username: str
    is_banned: bool
    role: RoleRead


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- posts ---
class PostCreate(BaseModel):
    content: str = Field(min_length=1)


class PostUpdate(BaseModel):
    content: str = Field(min_length=1)


class PostRead(ORMModel):
    id: int
    author_id: int
    content: str


# --- ratings ---
class RatingSet(BaseModel):
    score: int = Field(ge=1, le=5)
    review_text: str | None = None


class RatingRead(ORMModel):
    user_id: int
    post_id: int
    score: int
    review_text: str | None
