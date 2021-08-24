from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr = None
    pw: str = None
    name: str = None


class UserToken(BaseModel):



class Token(BaseModel):
    Authorization: str = None

