from typing import Annotated, Iterator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.repositories import PostRepository, RatingRepository, UserRepository
from api.config import ADMIN_ROLE
from api.security import decode_access_token
from api.services import AuthService, PostService, RatingService, UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# --- сессия БД и репозитории ---
def get_db() -> Iterator[Session]:
    with SessionLocal() as db:
        yield db


DbDep = Annotated[Session, Depends(get_db)]


def get_user_repository(db: DbDep) -> UserRepository:
    return UserRepository(db)


def get_post_repository(db: DbDep) -> PostRepository:
    return PostRepository(db)


def get_rating_repository(db: DbDep) -> RatingRepository:
    return RatingRepository(db)


UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
PostRepoDep = Annotated[PostRepository, Depends(get_post_repository)]
RatingRepoDep = Annotated[RatingRepository, Depends(get_rating_repository)]


# --- сервисы ---
def get_auth_service(users: UserRepoDep) -> AuthService:
    return AuthService(users)


def get_user_service(users: UserRepoDep) -> UserService:
    return UserService(users)


def get_post_service(posts: PostRepoDep) -> PostService:
    return PostService(posts)


def get_rating_service(ratings: RatingRepoDep, posts: PostRepoDep) -> RatingService:
    return RatingService(ratings, posts)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
PostServiceDep = Annotated[PostService, Depends(get_post_service)]
RatingServiceDep = Annotated[RatingService, Depends(get_rating_service)]


# --- аутентификация и авторизация ---
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], users: UserRepoDep) -> User:
    invalid = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Недействительный или просроченный токен",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = decode_access_token(token)
    except jwt.InvalidTokenError:
        raise invalid
    user = users.get(user_id)
    if user is None:
        raise invalid
    if user.is_banned:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Аккаунт заблокирован")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def require_admin(user: CurrentUser) -> User:
    if user.role.name != ADMIN_ROLE:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Требуются права администратора")
    return user
