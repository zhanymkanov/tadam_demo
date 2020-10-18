from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, ValidationError, root_validator


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    @root_validator
    def email_or_phone_required(cls, values):
        email = values.get("email")
        phone = values.get("phone")

        if not email and not phone:
            raise ValidationError("Either email or phone must be defined.")

        return values


class UserRegister(UserBase):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str


class UserLogin(UserBase):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: str


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None


# Base Properties for models stored in DB
class UserInDBBase(UserBase):
    id: UUID4
    email: EmailStr
    phone: str


# Returned to Client
class UserResponse(UserInDBBase):
    pass


# Stored in DB
class UserInDB(UserInDBBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr
