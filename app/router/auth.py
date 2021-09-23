from datetime import datetime, timedelta

import bcrypt
import jwt

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from decouple import config
from app.database.schema import UserSchema
from app.errors.exceptions import AlreadyExistEmailEx
from app.model import Token, UserRegister, UserToken, UserLogin
from app.repository.User import User
from app.utils.date_utils import D

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")

router = APIRouter(prefix="/auth")


@router.post("/register", status_code=201, response_model=Token)
async def register(reg_info: UserRegister):
    """
    '회원가입 API'\n
    :param reg_info:
    :return:
    """
    if not reg_info.email or not reg_info.pw:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=dict(msg="Email and PW must be provided"))

    is_exist = await is_email_exist(reg_info.email)
    if is_exist:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=dict(msg="Email already exists."))
        # raise AlreadyExistEmailEx(reg_info.email)

    hash_pw = bcrypt.hashpw(reg_info.pw.encode("utf-8"), bcrypt.gensalt())
    new_user = await User.create(
        UserSchema(
            email = reg_info.email,
            name = reg_info.name,
            pw = hash_pw,
            nickname = reg_info.nickname,
            address = reg_info.address
        )
    )

    jwt_token = create_access_token(
        data=UserToken(**new_user).dict(exclude={"pw", "created_at"})
    )
    token = dict(Authorization=f"JWT {jwt_token}")

    return token

@router.post("/login", status_code=200, response_model=Token)
async def login(user_info: UserLogin):
    if not user_info.email or not user_info.pw:
        return JSONResponse(status_code=400, content=dict(msg="Email ans PW must be provided"))

    if (user := await User.get_by_email(email=user_info.email)) is None:
        return JSONResponse(status_code=404, content=dict(msg="NO_MATCH_USER"))

    is_verified = bcrypt.checkpw(user_info.pw.encode("utf-8"), user['pw'].encode("utf-8"))
    if not is_verified:
        return JSONResponse(status_code=404, content=dict(msg="NO_MATCH_USER"))

    jwt_token = create_access_token(
        data=UserToken(**user).dict(exclude={'pw', 'created_at'})
    )
    print(jwt_token)
    token = dict(Authorization=f"JWT {jwt_token}")
    return token


async def is_email_exist(email: str) -> bool:
    if await User.get_by_email(email):
        return True
    return False

def create_access_token(data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp" : D.kstnow() + timedelta(hours=expires_delta)})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt