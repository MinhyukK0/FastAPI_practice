import sys

from starlette import status

sys.path.append("..")

from starlette.responses import JSONResponse
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from service.user import create_user, create_user_token
from models.users import CreateUser

router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@router.post("/signup")
async def post_user(user: CreateUser):
    create_user(user=user)
    return JSONResponse(
        {"message": "SIGNUP_SUCCESS"}, status_code=status.HTTP_201_CREATED
    )


@router.post("/signin")
async def post_signin(form_data: OAuth2PasswordRequestForm = Depends()):
    signin_token = await create_user_token(form_data)

    return JSONResponse(
        {"message": "SIGNIN_SUCCESS", "token": signin_token},
        status_code=status.HTTP_200_OK,
    )
