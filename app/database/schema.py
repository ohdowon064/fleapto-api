import json
from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr

from app.model import UserToken
from app.utils.date_utils import D


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid objectid")
        return ObjectId(value)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class BaseConfig:
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}


class BaseSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=D.kstnow)


class UserSchema(BaseSchema):
    email: EmailStr = Field(...)
    pw: str = Field(...)
    name: str = Field(...)
    nickname: str = Field(...)
    address: str = Field(...)

    class Config(BaseConfig):
        schema_extra = {
            "example": {
                "email": "user111@gmail.com",
                "name" : "kimuser"
            }
        }


class ProductSchema(BaseSchema):
    product_name: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    seller: UserToken = Field(...)
    buyer: UserToken = Field(default=None)
    is_purchased: bool = Field(default=False)
    purchased_time: datetime = Field(default=None)
    img_url: str = Field(...)

    class Config(BaseConfig):
        schema_extra = {
            "example" : {
                "product_name" : "반포 아파트",
                "seller" : {
                    "email" : "example@gmail.com"
                }
            }
        }


