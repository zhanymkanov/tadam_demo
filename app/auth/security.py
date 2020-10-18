from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from jose import jwt

from app.config import JWT_ALG, JWT_EXP, JWT_SECRET


def hash_password(password: str):
    """Generates a hashed version of the provided password."""
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


def check_password(password: str, password_in_db: bytes):
    password = bytes(password, "utf-8")
    return bcrypt.checkpw(password, password_in_db)


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = timedelta(minutes=JWT_EXP)
):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALG)
