import asyncio
import os

from motor import motor_asyncio
from fastapi import HTTPException

from app.base import DB_ID, DB_PASSWORD

client = motor_asyncio.AsyncIOMotorClient(os.environ.get("DB_URL", f"mongodb+srv://{DB_ID}:{DB_PASSWORD}@fleapto.2ry04.mongodb.net/fleapto_dev?retryWrites=true&w=majority"))
db = client.fleapto_dev