import sys
from fastapi.exceptions import HTTPException
from pydantic import fields

from pydantic.main import BaseModel
from sqlalchemy.orm.relationships import remote
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_404_NOT_FOUND
from api.user import get_user_by_token, get_user_exception
sys.path.append("..")

from fastapi import APIRouter, Depends
from pydantic.fields import Field
from sqlalchemy.orm import Session
from database import SessionLocal
from models import models

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix='/account',
    tags=['account'],
    responses={401 : {"account" : "invalid"}}
)

class Account(BaseModel):
    price : int = Field(gt=0)
    memo : str = Field(max_length=500)


@router.post('')
async def create_account(
                        account: Account,
                        user: dict = Depends(get_user_by_token),
                        db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    account_model = models.Account()
    account_model.price = account.price
    account_model.memo = account.memo
    account_model.user_id = user.get("id")

    db.add(account_model)
    db.commit()

    return JSONResponse({"message" : "CREATE_SUCCESS"}, status_code=201)


@router.get('')
async def get_all_accounts(user: dict = Depends(get_user_by_token), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    accounts = db.query(models.Account).filter(models.Account.user_id == user.get('id'), models.Account.is_removed == False).all()
    results = [{"id" : account.id, "금액" : account.price, "메모" : account.memo, "사용자" : account.user.username}for account in accounts]
    return JSONResponse({"result" : results}, status_code = 200)

@router.put('/{account_id}')
async def create_account(
                        account: Account,
                        account_id : int,
                        user: dict = Depends(get_user_by_token),
                        db: Session = Depends(get_db)):
    
    account_model = db.query(models.Account).filter(models.Account.id == account_id, models.Account.user_id == user.get('id')).first()

    if account_model is None:
        return get_user_exception()

    account_model.price = account.price
    account_model.memo = account.memo
    account_model.user_id = user.get("id")

    db.add(account_model)
    db.commit()

    return JSONResponse({"message" : "UPDATE_SUCCESS"}, status_code=201)

@router.delete('/{account_id}')
async def delete_selected_account(
                                account_id : int,
                                user : dict = Depends(get_user_by_token),
                                db : Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id, models.Account.user_id == user.get('id')).first()

    if account is None:
        raise item_not_found()
    
    account.is_removed = True

    db.commit()

    return JSONResponse({"message" : "DELETE_SUCCESS"}, status_code=200)

@router.get('/removed')
async def get_removed_account(user : dict = Depends(get_user_by_token), db : Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    accounts = db.query(models.Account).filter(models.Account.user_id == user.get('id'), models.Account.is_removed == True).all()
    results = [{"id" : account.id, "금액" : account.price, "메모" : account.memo, "사용자" : account.user.username}for account in accounts]
    return JSONResponse({"result" : results}, status_code = 200)

@router.patch('/removed/{account_id}')
async def restore_account(account_id : int ,user : dict = Depends(get_user_by_token), db : Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    account = db.query(models.Account).filter(models.Account.id == account_id,models.Account.user_id == user.get("id"),models.Account.is_removed == True).first()
    
    if account is None:
        raise item_not_found()

    account.is_removed = False  
    db.commit()
    
    return JSONResponse({"message" : "RESTORE_SUCCESS"}, status_code= 200)


def item_not_found():
    item_exception = HTTPException(
        status_code=404,
        detail="ITEM_NOT_FOUND"
    )
    return item_exception