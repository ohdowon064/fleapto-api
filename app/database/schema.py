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
    created_at: datetime = Field(default=D.kstnow())


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
    # 이름, 실제주소, 계좌주소, 사진, 올린사람정보, 가격, 판매여부
    product_name: str = Field(...)
    location: str = Field(...)
    address: str = Field(...)
    image: str = Field(...)
    seller: UserToken = Field(...)
    buyer: UserToken = Field(...)
    price: float = Field(...)
    is_saled: bool = Field(...)

    class Config(BaseConfig):
        schema_extra = {
            "example" :
        }



class TransactionSchema(BaseSchema):
    pass