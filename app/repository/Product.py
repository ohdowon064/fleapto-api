from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from app.database.connect import Mongo
from app.database.schema import ProductSchema
from app.errors import exceptions
from app.model import ProductRegister, UserToken
from app.repository.User import User
from app.utils.date_utils import D
from app.utils.s3_utils import S3


class Product:
    def __init__(self):
        self.db: AsyncIOMotorDatabase = Mongo.get_db()
        self.product_coll: AsyncIOMotorCollection = self.db.get_collection("products")


    @classmethod
    async def create(cls, file: UploadFile, product_info: ProductRegister, user):
        if (obj_url := S3.upload_file_to_bucket(
            file=file,
        )) is None:
            return None

        seller_info = user.dict()
        seller_info["_id"] = seller_info["id"]

        product = ProductSchema(
            product_name=product_info.product_name,
            description=product_info.description,
            seller=seller_info,
            img_url=obj_url
        )

        product_json = jsonable_encoder(product)
        inserted_product = await cls().product_coll.insert_one(product_json)
        new_product = await cls().product_coll.find_one({"_id" : inserted_product.inserted_id})
        return new_product


    @classmethod
    async def get_by_id(cls, id: str):
        if(product := await cls().product_coll.find_one({"_id" : id})) is None:
            raise exceptions.NotFoundEx
        return product


    @classmethod
    async def get_all(cls):
        product_cursor = cls().product_coll.find({}).sort("created_at")

        product_list = []
        async for product in product_cursor:
            product_list.append(product)

        return product_list

    @classmethod
    async def buy(cls, product_id: str, buyer: UserToken):
        product = await cls().get_by_id(product_id)

        buyer_info = buyer.dict()
        buyer_info["_id"] = buyer_info["id"]

        update_result = await cls().product_coll.find_one_and_update(
            {"_id" : product["_id"]}, {
                "$set" : {
                    "is_purchased" : True,
                    "purchased_time" : str(D.kstnow()),
                    "buyer" : buyer_info
                }
            }
        )

        updated_product = await cls().get_by_id(update_result["_id"])

        return updated_product

    @classmethod
    async def get_purchased_product(cls):
        product_cursor = cls().product_coll.find({"is_purchased" : True})
        product_list = [product async for product in product_cursor]
        return product_list


    @classmethod
    async def get_sales_history(cls, seller_id):
        product_cursor = cls().product_coll.find({
            "seller._id" : seller_id,
            "is_purchased" : True
        })
        product_list = [product async for product in product_cursor]
        return product_list

    @classmethod
    async def get_purchase_history(cls, buyer_id):
        product_cursor = cls().product_coll.find({
            "is_purchased" : True,
            "buyer._id" : buyer_id
        })
        product_list = [product async for product in product_cursor]
        return product_list