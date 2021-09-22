import asyncio
import json
import logging
from collections import Generator
from os import environ

import bcrypt
import pytest
from httpx import AsyncClient

from app.database.connect import Mongo
from app.database.schema import UserSchema
from app.model import UserToken
from app.repository.User import User
from app.router.auth import create_access_token
from main import create_app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def app():
    environ['STAGE'] = 'test'
    return create_app()

@pytest.fixture(scope="module")
async def client(app) -> Generator:
    async with AsyncClient(app=app, base_url="http://testserver") as _client:
        yield _client
    db = Mongo.get_db()
    await clear_all_table_data(db)

@pytest.fixture(scope="function")
async def user_info():
    """
    테스트 유저 정보
    :return:
    """
    return dict(
        email="test@example.com",
        pw="test",
        name="김테스트",
        nickname="김피누코인",
        address="ethereum-public-address"
    )

@pytest.fixture(scope="function")
async def create_user(user_info):
    origin_pw = user_info['pw']
    hash_pw = bcrypt.hashpw(origin_pw.encode("utf-8"), bcrypt.gensalt())
    db_user = await User.create(
        UserSchema(
            email=user_info['email'],
            name=user_info['name'],
            pw=hash_pw,
            nickname=user_info['nickname'],
            address=user_info['address']
        )
    )

    return db_user, origin_pw

@pytest.fixture(scope="function")
async def login(create_user):
    """
    테스트전 로그인을 위한 사용자 등록
    :return:
    """
    db_user, origin_pw = create_user
    access_token = create_access_token(
        data=UserToken(**db_user).dict(exclude={"pw", "created_at"})
    )
    token = dict(Authorization=f"JWT {access_token}")

    return token

@pytest.fixture(scope="function")
async def db_product(client, login):
    """
    테스트전 상품 추가
    :param login:
    :return:
    """
    files = dict(file=open("./test.jpg", "rb"))
    data = dict(product_name="test", description="test", price="1.25", seller_safe=True)
    payload = dict(product_info=json.dumps(data))

    res = await client.post("/api/product", files=files, data=payload, headers=login)
    res_body = res.json()
    return res_body


async def clear_all_table_data(db):
    logging.info("Drop Test Database")
    coll_names = await db.list_collection_names()
    for coll_name in coll_names:
        await db.drop_collection(coll_name)
