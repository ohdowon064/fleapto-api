from pydantic import BaseModel, EmailStr


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
    id: str = None
    email: str = None
    name: str = None
    nickname: str = None
    address: str = None

    class Config:
        orm_mode = True


class UserMe(BaseModel):
    id: str = None
    email: str = None
    name: str = None


class Token(BaseModel):
    Authorization: str = None

