from os import getenv

import pytest
from httpx import AsyncClient

from app.database.schema import UserSchema
from app.repository.User import User


@pytest.mark.asyncio
async def test_register(client, user_info):
    """
    회원가입 테스트
    :param client:
    :param db:
    :return:
    """

    res = await client.post("/api/auth/register", json=user_info)
    res_body = res.json()

    assert res.status_code == 201
    assert "Authorization" in res_body.keys()


@pytest.mark.asyncio
async def test_register_exist_email(client, create_user):
    """
    이미 존재하는 이메일 테스트
    :param client:
    :return:
    """
    db_user, origin_pw = create_user

    res = await client.post("/api/auth/register", json=db_user)
    res_body = res.json()

    print(res_body)

    assert getenv("STAGE") == "test"
    assert res.status_code == 400
    assert res_body == {"msg" : "Email already exists."}


@pytest.mark.asyncio
async def test_login(client: AsyncClient, create_user):
    """
    로그인 테스트
    :param client:
    :return:
    """
    db_user, origin_pw = create_user
    login_info = dict(email=db_user["email"], pw=origin_pw)

    res = await client.post("/api/auth/login", json=login_info)
    res_body = res.json()

    assert res.status_code == 200
    assert "Authorization" in res_body.keys()

@pytest.mark.asyncio
async def test_login_not_exist_email(client: AsyncClient):
    """
    존재하지 않는 이메일 로그인
    :param client:
    :return:
    """

    login_info = dict(email="notexist@example.com", pw="test")

    res = await client.post("/api/auth/login", json=login_info)
    res_body = res.json()

    assert res.status_code == 404
    assert res_body == {"msg" : "NO_MATCH_USER"}


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, create_user):
    """
    올바르지 않은 패스워드
    :param client:
    :return:
    """
    db_user, origin_pw = create_user

    login_info = dict(email=db_user["email"], pw="wrongpw")

    res = await client.post("/api/auth/login", json=login_info)
    res_body = res.json()

    assert res.status_code == 404
    assert res_body == {"msg" : "NO_MATCH_USER"}
