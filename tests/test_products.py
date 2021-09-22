import json

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_product(client: AsyncClient, login):
    """
    상품 생성 테스트
    :param client:
    :param login:
    :return:
    """
    files = dict(file=open("./test.jpg", "rb"))
    data = dict(product_name="test", description="test", price="1.25", seller_safe=True)
    payload = dict(product_info=json.dumps(data))

    res = await client.post("/api/product", files=files, data=payload, headers=login)
    res_body = res.json()

    assert res.status_code == 201, res_body


@pytest.mark.asyncio
async def test_pending_product(client: AsyncClient, login, db_product):
    """
    상품 구매 테스트
    :param client:
    :param login:
    :return:
    """
    product_state = dict(state="PENDING")
    res = await client.put(f"/api/product?product_id={db_product['_id']}", json=product_state, headers=login)
    res_body = res.json()

    assert res.status_code == 200, res_body
    assert res_body["state"] == "PENDING"

@pytest.mark.asyncio
async def test_reject_product(client: AsyncClient, login, db_product):
    """
    상품 구매 테스트
    :param client:
    :param login:
    :return:
    """
    product_state = dict(state="REJECTED")
    res = await client.put(f"/api/product?product_id={db_product['_id']}", json=product_state, headers=login)
    res_body = res.json()

    assert res.status_code == 200, res_body
    assert res_body["state"] == "SALE"

@pytest.mark.asyncio
async def test_buy_product(client: AsyncClient, login, db_product):
    """
    상품 구매 테스트
    :param client:
    :param login:
    :return:
    """
    product_state = dict(state="SOLD")
    res = await client.put(f"/api/product?product_id={db_product['_id']}", json=product_state, headers=login)
    res_body = res.json()

    assert res.status_code == 200, res_body
    assert res_body["state"] == "SOLD"