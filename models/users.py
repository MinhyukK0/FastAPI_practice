import sys


sys.path.append("..")

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .accounts import Account


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
