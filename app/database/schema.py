from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr

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

class BaseConfing:
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders = {ObjectId: str}

class UserSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr = Field(...)
    pw: str = Field(...)
    name: str = Field(...)
    nickname: str = Field(...)
    address: str = Field(...)
    created_at: datetime = Field(default=D.kstnow())


    class Config(BaseConfing):
        schema_extra = {
            "example": {
                "email": "user111@gmail.com",
                "name" : "kimuser"
            }
        }