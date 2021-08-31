from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from app.database.connect import db
from app.database.schema import UserSchema
from app.model import UserRegister


class User:
    user_coll: AsyncIOMotorCollection = db.get_collection("users")

    @classmethod
    async def create(cls, user: UserSchema):
        user_json = jsonable_encoder(user)
        inserted_user = await cls.user_coll.insert_one(user_json)
        new_user = await cls.user_coll.find_one({"_id" : inserted_user.inserted_id})

        return new_user

    @classmethod
    async def get_by_id(cls, id: str):
        user = await cls.user_coll.find_one({"_id" : id})
        return user

    @classmethod
    async def get_by_email(cls, email: str):
        user = await cls.user_coll.find_one({"email" : email})
        return user

    @classmethod
    async def delete_by_id(cls, id: str):
        deleted_user = await cls.user_coll.find_one_and_delete({"_id": id})
        return deleted_user
