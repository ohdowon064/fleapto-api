from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from app.database.connect import Mongo
from app.database.schema import ProductSchema, State, PendingSchema
from app.errors import exceptions
from app.model import ProductRegister, UserToken
from app.repository.User import User
from app.utils.date_utils import D
from app.utils.s3_utils import S3
from app.errors.exceptions import CanNotDeleteProductEx, FailToDeleteProductEx


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
            price=product_info.price,
            seller=seller_info,
            seller_safe=product_info.seller_safe,
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
        buyer_info["_id"] = buyer_info.pop("id")

        if product['state'] == State.PENDING:
            pending_coll = cls().db.get_collection("pending")
            pending = await pending_coll.find_one_and_update(
                {"product_id": product_id}, {
                    "$set": {"state": State.SOLD}
                }
            )

        query = dict(purchased_time = str(D.kstnow()),
                     state = State.SOLD,
                     buyer=buyer_info)

        update_result = await cls().product_coll.find_one_and_update(
            {"_id" : product["_id"]}, {
                "$set" : query
            }
        )

        updated_product = await cls().get_by_id(update_result["_id"])

        return updated_product

    @classmethod
    async def pending(cls, product_id: str, buyer: UserToken):
        product = await cls().get_by_id(product_id)

        update_result = await cls().product_coll.find_one_and_update(
            {"_id" : product["_id"]}, {
                "$set" : {"state" : State.PENDING}
            }
        )

        updated_product = await cls().get_by_id(update_result["_id"])

        buyer_info = buyer.dict()
        buyer_info["_id"] = buyer_info.pop("id")

        pending = PendingSchema(
            product_id = product_id,
            buyer = buyer,
            extra_price = product["price"] * 0.05
        )

        pending_json = jsonable_encoder(pending)

        pending_coll = cls().db.get_collection("pending")
        inserted_pending = await pending_coll.insert_one(pending_json)

        return updated_product


    @classmethod
    async def reject(cls, product_id):
        pending_coll = cls().db.get_collection("pending")
        pending = await pending_coll.find_one_and_update(
            {"product_id": product_id}, {
                "$set": {"state": State.REJECTED}
            }
        )

        product = await cls().product_coll.find_one_and_update(
            {"_id": product_id}, {
                "$set": {"state": State.SALE}
            }
        )

        return product



    @classmethod
    async def get_purchased_product(cls):
        product_cursor = cls().product_coll.find({"is_purchased" : True})
        product_list = [product async for product in product_cursor]
        return product_list


    @classmethod
    async def get_sales_history(cls, seller_id):
        product_cursor = cls().product_coll.find({
            "seller._id" : seller_id,
            "state" : "SOLD"
        })
        product_list = [product async for product in product_cursor]
        return product_list

    @classmethod
    async def get_purchase_history(cls, buyer_id):
        product_cursor = cls().product_coll.find({
            "buyer._id" : buyer_id,
            "state": "SOLD"
        })
        product_list = [product async for product in product_cursor]
        return product_list


    @classmethod
    async def delete(cls, product_id: str, request_id: str):
        if (to_delete := await cls.get_by_id(product_id)) is None:
            return None

        seller_id = to_delete["seller"]["_id"]
        if request_id != seller_id:
            raise CanNotDeleteProductEx()

        deleted_product = await cls().product_coll.delete_one({"_id" : to_delete["_id"]})

        if deleted_product.deleted_count != 1:
            raise FailToDeleteProductEx(product_id)

        return deleted_product.deleted_count


    @classmethod
    async def buyer_safe_or_not(cls, product_id: str, buyer_safe: bool):
        updated_result = await cls().product_coll.find_one_and_update(
            {"_id": product_id}, {
                "$set": {"buyer_safe": buyer_safe}
            }
        )

        product = await cls().get_by_id(product_id)
        return product

    @classmethod
    async def get_pending_list(cls, buyer_id: str):
        pending_cursor = cls().db.get_collection("pending").find(
            {"buyer._id": buyer_id, "state": State.PENDING}
        )

        product_ids = [product["product_id"] async for product in pending_cursor]

        product_cursor = cls().product_coll.find(
            {"_id": {"$in": product_ids}}
        )

        pending_list = [product async for product in product_cursor]

        return pending_list