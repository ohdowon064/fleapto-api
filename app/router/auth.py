from datetime import datetime, timedelta

import bcrypt
import jwt

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.base import JWT_SECRET, JWT_ALGORITHM
from app.database.connect import db
from app.database.schema import UserSchema
from model import Token, UserRegister

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

    hash_pw = bcrypt.hashpw(reg_info.pw.encode("utf-8"), bcrypt.gensalt())
    new_user = UserSchema(
        email = reg_info.email,
        name = reg_info.name,
        pw = hash_pw
    )
    jwt_token = create_access_token(data=)
    token = dict(Authorization=f"Bearer {}")

    return "check"


async def is_email_exist(email: str) -> bool:
    if db['users'].find_one({"email": email}):
        return True
    return False

def create_access_token(data: dict = None, expires_delta: int = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp" : datetime.utcnow() + timedelta(hours=expires_delta)})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)