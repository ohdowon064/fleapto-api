from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr = None
    pw: str = None
    name: str = None
    nickname: str = None
    address: str = None


class UserLogin(BaseModel):
    email: EmailStr = None
    pw: str = None


class UserToken(BaseModel):
    id: str = Field(None, alias="_id")
    email: str = None
    name: str = None
    nickname: str = None
    address: str = None


class Token(BaseModel):
    Authorization: str = None