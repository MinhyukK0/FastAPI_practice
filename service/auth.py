import sys

sys.path.append("..")

from fastapi import Depends, HTTPException, status
from typing import Optional
from models import users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from database import engine

SECRET_KEY = "CSrZ55fe7tVW-FT7kD0NMCE6pLsNCLzHLyIktjr5riI"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

session = Session(bind=engine)


def hash_password(password):
    return bcrypt_context.hash(password)


def verify_password(password, hashed_password):
    return bcrypt_context.verify(password, hashed_password)


def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response


def authenticate_user(username: str, password: str):
    user = session.query(users.User).filter(users.User.username == username).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None):
    payload = {"id": user_id}

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=20)

    payload.update({"exp": expire})

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_user_by_token(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")

        if user_id is None:
            raise token_exception()

        return {"id": user_id}

    except JWTError:
        raise token_exception()
