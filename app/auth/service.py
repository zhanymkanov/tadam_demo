from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.config import JWT_ALG, JWT_SECRET

from . import users
from .constants import ErrorCode
from .models import TokenData, UserLogin
from .security import check_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_jwt_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorCode.COULD_NOT_VALIDATE_CREDENTIALS,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except JWTError:
        raise credentials_exception

    email: str = payload.get("sub")
    if not email:
        raise credentials_exception

    token_data = TokenData(email=email)
    user = await users.get_by_email(email=token_data.email)
    if not user:
        raise credentials_exception

    return user


async def get_jwt_user_active(current_user=Depends(get_jwt_user)):
    if not current_user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=ErrorCode.USER_IS_NOT_ACTIVE
        )
    return current_user


async def authenticate(*, user_in: UserLogin):
    user = await users.get_by_email(user_in.email)
    if not user or not check_password(user_in.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.COULD_NOT_VALIDATE_CREDENTIALS,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
