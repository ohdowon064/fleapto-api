import json
from dataclasses import dataclass

from fastapi import UploadFile, File
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


class ProductRegister(BaseModel):
    product_name: str = None
    description: str = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value