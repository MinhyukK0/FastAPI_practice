from datetime import datetime
import sys
sys.path.append("..")

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index= True)
    username = Column(String(50), unique=True)
    email = Column(String(300), unique=True)
    password = Column(String(2000))

    account = relationship("Account", back_populates="user")


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index= True)
    price = Column(Integer)
    memo = Column(String(500), default="")
    user_id  = Column(Integer, ForeignKey("users.id"))
    is_removed = Column(Boolean, default=False)
    created_at = Column(DateTime, default = datetime.now())
    updated_at = Column(DateTime, default = datetime.now())

    user = relationship("User", back_populates="account")
