from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import AuthServiceDep
from api.schemas import Token, UserCreate, UserRead

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: UserCreate, service: AuthServiceDep):
    return service.register(data)


@router.post("/login", response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], service: AuthServiceDep):
    return service.login(form.username, form.password)
