import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, login):
    """
    유저 잔액 업데이트 테스트
    :param client:
    :param login:
    :return:
    """
    update_info = dict(balance=70)

    res = await client.put("/api/user", json=update_info, headers=login)
    res_body = res.json()

    assert res.status_code == 200, res_body


@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, login):
    """
    유저 정보 검색
    :param client:
    :param login:
    :return:
    """

    res = await client.get("/api/me", headers=login)
    res_body = res.json()

    assert res.status_code == 200, res_body
