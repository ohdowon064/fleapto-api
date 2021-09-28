from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from app.database.connect import Mongo
from app.database.schema import UserSchema
from app.errors.exceptions import AlreadyExistEmailEx
from app.model import UserToken, UserUpdate


class User:
    # db: AsyncIOMotorDatabase = connection.get_db()
    # user_coll: AsyncIOMotorCollection = db.get_collection("users")

    def __init__(self):
        self.db: AsyncIOMotorDatabase = Mongo.get_db()
        self.user_coll: AsyncIOMotorCollection = self.db.get_collection("users")

    @classmethod
    async def create(cls, user: UserSchema):
        user_json = jsonable_encoder(user)
        inserted_user = await cls().user_coll.insert_one(user_json)
        new_user = await cls().user_coll.find_one({"_id" : inserted_user.inserted_id})

        return new_user

    @classmethod
    async def get_by_id(cls, id: str):
        user = await cls().user_coll.find_one({"_id" : id})
        return user

    @classmethod
    async def get_by_email(cls, email: str):
        user = await cls().user_coll.find_one({"email" : email})
        return user

    @classmethod
    async def get_info(cls, id: str):
        if (user := await cls().user_coll.find_one({"_id" : id})) is None:
            return None
        user_info = UserToken(**user).dict(exclude={"pw", "created_at"})
        return user_info

    @classmethod
    async def delete_by_id(cls, id: str):
        deleted_user = await cls().user_coll.find_one_and_delete({"_id": id})
        return deleted_user

    @classmethod
    async def update(cls, user_id: str, update_info: UserUpdate):
        prev_user = await cls().user_coll.find_one_and_update(
            {"_id": user_id}, {
                "$set": {**update_info.dict()}
            }
        )

        updated_user = await cls().get_by_id(user_id)

        return updated_user

