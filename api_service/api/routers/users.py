from fastapi import APIRouter, Depends, status

from api.dependencies import CurrentUser, UserServiceDep, require_admin
from api.schemas import UserRead

router = APIRouter(tags=["users"])


@router.get("/users", response_model=list[UserRead], dependencies=[Depends(require_admin)])
def list_users(service: UserServiceDep):
    return service.list_users()


@router.post("/users/{user_id}/ban", response_model=UserRead, dependencies=[Depends(require_admin)])
def ban_user(user_id: int, service: UserServiceDep):
    return service.set_banned(user_id, True)


@router.post("/users/{user_id}/unban", response_model=UserRead, dependencies=[Depends(require_admin)])
def unban_user(user_id: int, service: UserServiceDep):
    return service.set_banned(user_id, False)


@router.post("/users/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
def follow(user_id: int, current_user: CurrentUser, service: UserServiceDep):
    service.follow(current_user, user_id)


@router.delete("/users/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
def unfollow(user_id: int, current_user: CurrentUser, service: UserServiceDep):
    service.unfollow(current_user, user_id)
