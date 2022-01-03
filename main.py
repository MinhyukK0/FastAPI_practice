from fastapi import FastAPI, Depends
from models import models
from database import engine
from api import user, account

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

app.include_router(user.router)
app.include_router(account.router)