from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from . import service, users
from .models import Token, UserLogin, UserRegister, UserResponse
from .security import create_access_token

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_in = UserLogin(email=form_data.username, password=form_data.password)
    user = await service.authenticate(user_in=user_in)
    return {
        "access_token": create_access_token(data={"sub": user["email"]}),
        "token_type": "bearer",
    }


@router.post("/register", response_model=Token)
async def register(user_in: UserRegister):
    user_email = await users.create(user_in=user_in)
    return {
        "access_token": create_access_token(data={"sub": user_email}),
        "token_type": "bearer",
    }


@router.post("/users/me", response_model=UserResponse)
def read_users_me(current_user=Depends(service.get_jwt_user_active)) -> Any:
    """
    Test access token
    """
    return current_user
