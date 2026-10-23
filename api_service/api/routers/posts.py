from fastapi import APIRouter, status

from api.dependencies import CurrentUser, PostServiceDep
from api.schemas import PostCreate, PostRead, PostUpdate

router = APIRouter(tags=["posts"])


@router.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(data: PostCreate, user: CurrentUser, service: PostServiceDep):
    return service.create(user, data)


@router.get("/posts", response_model=list[PostRead])
def list_posts(user: CurrentUser, service: PostServiceDep):
    return service.list_posts()


@router.get("/feed", response_model=list[PostRead])
def get_feed(user: CurrentUser, service: PostServiceDep):
    return service.feed(user)


@router.get("/posts/{post_id}", response_model=PostRead)
def get_post(post_id: int, user: CurrentUser, service: PostServiceDep):
    return service.get(post_id)


@router.patch("/posts/{post_id}", response_model=PostRead)
def update_post(post_id: int, data: PostUpdate, user: CurrentUser, service: PostServiceDep):
    return service.update(user, post_id, data)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, user: CurrentUser, service: PostServiceDep):
    service.delete(user, post_id)
