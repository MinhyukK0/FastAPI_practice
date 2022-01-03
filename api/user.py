import sys
sys.path.append("..")

from pydantic.fields import Field
from starlette.responses import JSONResponse


from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import Optional
from models import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = "CSrZ55fe7tVW-FT7kD0NMCE6pLsNCLzHLyIktjr5riI"
ALGORITHM = "HS256"

class CreateUser(BaseModel):
    username : str
    email : str = Field(regex="[a-zA-Z0-9]+\.?\w*@\w+[.]?\w*[.]+\w{2,3}")
    password : str = Field(regex="(?=.*[A-Za-z])(?=.*\d)(?=.*[~!@#$^&*()+|=])[A-Za-z\d~!@#$%^&*()+|=]{8,}")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/users",
    tags=["user"],
    responses={401: {"user" : "Not authorized"}},
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def password_hash(password):
    return bcrypt_context.hash(password)

def verify_password(password, hashed_password):
    return bcrypt_context.verify(password, hashed_password)

def authenticate_user(username : str, password: str, db):
    user = db.query(models.User).filter(models.User.username == username).first()
    
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(user_id : int, expires_delta: Optional[timedelta]=None):
    payload = {"id" : user_id}
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=20)
    
    payload.update({"exp" :expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id : int = payload.get("id")
        
        if user_id is None:
            raise get_user_exception()
        
        return {"user_id" : user_id}
    
    except JWTError:
        raise get_user_exception()

@router.post("/signup")
async def user_signup(user : CreateUser, db: Session = Depends(get_db)):
    new_user_model = models.User() 
    new_user_model.username = user.username
    new_user_model.email = user.email
    new_user_model.password = password_hash(user.password)

    db.add(new_user_model)
    db.commit()
    return JSONResponse({"message" : "SIGNUP_SUCCESS"},status_code=201)

@router.post("/signin")
async def user_signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise get_user_exception()

    token_expire = timedelta(minutes= 20)
    token = create_access_token(user.id, token_expire)

    return JSONResponse({"message" : "SIGNIN_SUCCESS", "token" : token}, status_code=200)


# Token Decorator
async def get_user_by_token(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")

        if user_id is None:
            raise token_exception()
        
        return {"id": user_id}
    
    except JWTError:
        raise token_exception()

#Exceptions
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