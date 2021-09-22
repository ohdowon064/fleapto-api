from datetime import datetime
from enum import Enum

from pydantic import EmailStr, Field

from app.database.base_schema import BaseSchema
from app.model import UserToken


class UserSchema(BaseSchema):
    email: EmailStr = Field(...)
    pw: str = Field(...)
    name: str = Field(...)
    nickname: str = Field(...)
    address: str = Field(...)


class State(str, Enum):
    SALE = 'SALE'
    PENDING = 'PENDING'
    REJECTED = 'REJECTED'
    SOLD = 'SOLD'

class ProductSchema(BaseSchema):
    product_name: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    seller: UserToken = Field(...)
    buyer: UserToken = Field(default=None)
    state: State = Field(default=State.SALE) # is_purchased -> state
    purchased_time: datetime = Field(default=None)
    img_url: str = Field(...)
    seller_safe: bool = Field(...)
    buyer_safe: bool = Field(default=False)


class PendingSchema(BaseSchema):
    product_id: str = Field(...)
    buyer: UserToken = Field(...)
    extra_price: float = Field(...)
    state: State = Field(default=State.PENDING)