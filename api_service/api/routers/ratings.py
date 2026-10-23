from fastapi import APIRouter, Depends, status

from api.dependencies import CurrentUser, RatingServiceDep, require_admin
from api.schemas import RatingRead, RatingSet

router = APIRouter(tags=["ratings"])


@router.put("/posts/{post_id}/rating", response_model=RatingRead)
def set_rating(post_id: int, data: RatingSet, user: CurrentUser, service: RatingServiceDep):
    return service.set_rating(user, post_id, data)


@router.get("/posts/{post_id}/ratings", response_model=list[RatingRead])
def list_ratings(post_id: int, user: CurrentUser, service: RatingServiceDep):
    return service.list_for_post(post_id)


@router.delete(
    "/posts/{post_id}/ratings/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_admin)],
)
def delete_rating(post_id: int, user_id: int, service: RatingServiceDep):
    service.delete(post_id, user_id)
