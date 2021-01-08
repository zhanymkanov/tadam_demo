import uuid

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import UUID4, EmailStr

from app.database import database, users

from .constants import ErrorCode
from .models import UserRegister
from .security import hash_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


async def get(user_id: UUID4):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


async def get_by_email(email: EmailStr):
    query = users.select().where(users.c.email == email)
    return await database.fetch_one(query)


async def get_by_phone(phone: str):
    query = users.select().where(users.c.phone == phone)
    return await database.fetch_one(query)


async def get_by_email_or_phone(*, email: EmailStr, phone: str):
    query = users.select().where((users.c.email == email) | (users.c.phone == phone))
    return await database.fetch_one(query)


async def exists(*, email: EmailStr = None, phone: str = None):
    if email and phone:
        return await get_by_email_or_phone(email=email, phone=phone)

    if email:
        return await get_by_email(email)

    if phone:
        return await get_by_phone(phone)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=ErrorCode.PHONE_OR_EMAIL_IS_REQUIRED,
    )


async def create(*, user_in: UserRegister):
    if await exists(email=user_in.email, phone=user_in.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.REGISTER_USER_ALREADY_EXISTS,
        )

    query = (
        users.insert()
        .values(
            **user_in.dict(exclude={"password"}),
            password=hash_password(user_in.password),
            id=uuid.uuid4()
        )
        .returning(users.c.email)
    )

    return await database.execute(query)
