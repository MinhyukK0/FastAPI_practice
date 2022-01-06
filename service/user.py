import sys

sys.path.append("..")

from service.auth import (
    authenticate_user,
    create_access_token,
    get_user_exception,
    hash_password,
)
from fastapi import Depends
from models.users import User
from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from models.users import CreateUser


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    new_user = User()
    new_user.username = user.username
    new_user.email = user.email
    new_user.password = hash_password(user.password)

    db.add(new_user)
    db.commit()


async def create_user_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise get_user_exception()

    token_expire = timedelta(minutes=20)
    token = create_access_token(user.id, token_expire)

    return token
