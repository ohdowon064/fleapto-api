import logging
from typing import List

from fastapi import APIRouter, UploadFile, File, Form, Body, Depends
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.database.schema import ProductSchema, State
from app.model import ProductRegister, ProductState
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
async def update_product(request: Request, product_id: str, product_state: ProductState = Body(...)):
    buyer = request.state.user
    state = product_state.state

    if state == State.PENDING:
        updated_product = await Product.pending(product_id, buyer)
    elif state == State.SOLD:
        updated_product = await Product.buy(product_id, buyer)
    elif state == State.REJECTED:
        updated_product = await Product.reject(product_id)
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content="올바르지 않은 상태값입니다. SOLD, PENDING, REJECTED 중에 가능합니다.")

    return updated_product

@router.put("/product/{product_id}", status_code=200, response_model=ProductSchema)
async def buyer_safe_or_not(request: Request, product_id: str, buyer_safe: bool):
    buyer = request.state.user
    product = await Product.buyer_safe_or_not(product_id, buyer_safe)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=product
    )

@router.delete("/product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(request: Request, product_id: str):
    user = request.state.user
    deleted_count = await Product.delete(product_id, user.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(msg=f"{deleted_count}개의 상품을 성공적으로 삭제했습니다."))