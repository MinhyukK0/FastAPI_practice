import sys

sys.path.append("..")

from fastapi.exceptions import HTTPException
from datetime import datetime
from service.auth import get_user_exception
from sqlalchemy.orm import Session
from database import engine
from models import models
from models.models import CreateAccount

session = Session(bind=engine)


def item_not_found():
    item_exception = HTTPException(status_code=404, detail="ITEM_NOT_FOUND")
    return item_exception


def create_account(account: CreateAccount, user: dict):
    if user is None:
        raise get_user_exception()

    account_model = models.Account()
    account_model.price = account.price
    account_model.memo = account.memo
    account_model.user_id = user.get("id")

    session.add(account_model)
    session.commit()


def read_accounts(user: dict):
    if user is None:
        raise get_user_exception()

    accounts = (
        session.query(models.Account)
        .filter(
            models.Account.user_id == user.get("id"), models.Account.is_removed == False
        )
        .all()
    )
    results = [
        {
            "id": account.id,
            "금액": account.price,
            "메모": account.memo,
            "사용자": account.user.username,
        }
        for account in accounts
    ]

    return results


def update_account(account: CreateAccount, account_id: int, user: dict):
    user_id = user.get("id")

    if user_id is None:
        raise get_user_exception()

    account_model = (
        session.query(models.Account)
        .filter(models.Account.id == account_id, models.Account.user_id == user_id)
        .first()
    )

    if account_model is None:
        raise item_not_found()

    account_model.price = account.price
    account_model.memo = account.memo
    account_model.user_id = user_id
    account_model.updated_at = datetime.now()

    session.add(account_model)
    session.commit()


def remove_account(account_id: int, user: dict):
    user_id = user.get("id")

    if user_id is None:
        raise get_user_exception()

    account = (
        session.query(models.Account)
        .filter(
            models.Account.id == account_id, models.Account.user_id == user.get("id")
        )
        .first()
    )

    if account is None or account.is_removed == True:
        raise item_not_found()

    account.is_removed = True

    session.commit()


def read_removed_account(user: dict):
    user_id = user.get("id")

    if user_id is None:
        raise get_user_exception()

    accounts = (
        session.query(models.Account)
        .filter(models.Account.user_id == user_id, models.Account.is_removed == True)
        .all()
    )

    return [
        {
            "id": account.id,
            "금액": account.price,
            "메모": account.memo,
            "사용자": account.user.username,
        }
        for account in accounts
    ]


def update_removed_account(account_id: int, user: dict):
    user_id = user.get("id")

    if user_id is None:
        raise get_user_exception()

    account = (
        session.query(models.Account)
        .filter(
            models.Account.id == account_id,
            models.Account.user_id == user.get("id"),
            models.Account.is_removed == True,
        )
        .first()
    )

    if account is None or account.is_removed == False:
        raise item_not_found()

    account.is_removed = False
    session.commit()
