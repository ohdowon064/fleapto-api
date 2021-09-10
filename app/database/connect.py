import logging
import ssl
from os import environ

from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class Mongo:
    DB_URL = config("DB_URL")

    db_client = AsyncIOMotorClient(DB_URL, ssl_cert_reqs=ssl.CERT_NONE)
    print(f"{DB_URL} 엔드포인트.....")
    logging.debug("connected db")

    @classmethod
    async def disconnected_db(cls):
        cls.db_client.close()
        logging.debug("disconnected db")

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        STAGE = environ.get("STAGE", 'local')
        DB_NAME = config("DB_NAME").format(STAGE=STAGE)
        db = cls.db_client[DB_NAME]
        return db