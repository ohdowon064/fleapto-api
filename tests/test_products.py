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
    file = open("./test.jpg", "rb")
    product_info = dict(product_name="test", description="test")

    res = await client.post("/api/product", files=file, data=product_info, headers=login)
    res_body = res.json()

    assert res.status_code == 201
