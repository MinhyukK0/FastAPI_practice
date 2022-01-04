import sys


sys.path.append("..")

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel, Field
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(300), unique=True)
    password = Column(String(2000))

    account = relationship("Account", back_populates="user")


class CreateUser(BaseModel):
    username: str
    email: str = Field(regex="[a-zA-Z0-9]+\.?\w*@\w+[.]?\w*[.]+\w{2,3}")
    password: str = Field(
        regex="(?=.*[A-Za-z])(?=.*\d)(?=.*[~!@#$^&*()+|=])[A-Za-z\d~!@#$%^&*()+|=]{8,}"
    )


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Integer)
    memo = Column(String(500), default="")
    user_id = Column(Integer, ForeignKey("users.id"))
    is_removed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="account")


class CreateAccount(BaseModel):
    price: int = Field(gt=0)
    memo: str = Field(max_length=500)
