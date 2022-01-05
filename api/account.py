import sys

sys.path.append("..")

from pydantic.main import BaseModel
from starlette.responses import JSONResponse
from service.account import (
    create_account,
    read_accounts,
    read_removed_account,
    remove_account,
    update_account,
    update_removed_account,
)
from service.auth import get_user_by_token
from fastapi import APIRouter, Depends, status
from models.models import CreateAccount

router = APIRouter(prefix="/accounts", tags=["account"])


@router.post("")
async def post_account(account: CreateAccount, user: dict = Depends(get_user_by_token)):
    create_account(account=account, user=user)

    return JSONResponse(
        {"message": "CREATE_SUCCESS"}, status_code=status.HTTP_201_CREATED
    )


@router.get("")
async def get_accounts(user: dict = Depends(get_user_by_token)):
    results = read_accounts(user=user)

    return JSONResponse({"result": results}, status_code=status.HTTP_200_OK)


@router.put("/{account_id}")
async def put_account(
    account: CreateAccount, account_id: int, user: dict = Depends(get_user_by_token)
):
    update_account(account=account, account_id=account_id, user=user)

    return JSONResponse({"message": "UPDATE_SUCCESS"}, status_code=status.HTTP_200_OK)


@router.delete("/{account_id}")
async def delete_account(account_id: int, user: dict = Depends(get_user_by_token)):
    remove_account(account_id=account_id, user=user)

    return JSONResponse({"message": "DELETE_SUCCESS"}, status_code=status.HTTP_200_OK)


@router.get("/removed")
async def get_removed_accounts(user: dict = Depends(get_user_by_token)):

    results = read_removed_account(user=user)

    return JSONResponse({"result": results}, status_code=status.HTTP_200_OK)


@router.patch("/removed/{account_id}")
async def patch_removed_account(
    account_id: int, user: dict = Depends(get_user_by_token)
):
    update_removed_account(account_id=account_id, user=user)

    return JSONResponse({"message": "RESTORE_SUCCESS"}, status_code=status.HTTP_200_OK)
