from typing import List

from fastapi import APIRouter, UploadFile, File, Form, Body, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.database.schema import ProductSchema
from app.model import ProductRegister
from app.repository.Product import Product

router = APIRouter()

@router.post("/product", status_code=201, response_model=ProductSchema)
async def create_product(request: Request,
                         product_info: ProductRegister,
                         file: UploadFile = File(...)):

    user = request.state.user

    if (created_product := await Product.create(file, product_info, user)) is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="상품 등록에 실패했습니다."
        )

    return created_product


@router.get("/product", status_code=200, response_model=List[ProductSchema])
async def get_product():
    product_list = await Product.get_all()
    return product_list


@router.put("/product", status_code=200, response_model=ProductSchema)
async def update_product(request: Request, product_id: str):
    buyer = request.state.user
    updated_product = await Product.buy(product_id, buyer)
    return updated_product