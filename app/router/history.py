from typing import List

from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.database.schema import ProductSchema
from app.repository.Product import Product

router = APIRouter()

@router.get("/sales-history", response_model=List[ProductSchema])
async def search_sales_history(request: Request):
    seller = request.state.user
    print(seller)
    sales_list = await Product.get_sales_history(seller.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=sales_list
    )


@router.get("/purchase-history", response_model=List[ProductSchema])
async def search_purchase_history(request: Request):
    buyer = request.state.user
    print("buyer??????????", buyer)
    purchase_list = await Product.get_purchase_history(buyer.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=purchase_list
    )