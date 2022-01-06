import sys


sys.path.append("..")

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel, Field
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User


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
