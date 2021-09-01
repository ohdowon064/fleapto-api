from fastapi import APIRouter
from starlette.requests import Request

from app.model import UserToken
from app.repository.User import User

router = APIRouter()

@router.get("/me", response_model=UserToken)
async def get_user(request: Request):
    """
    get my info
    :param request:
    :return:
    """
    user = request.state.user
    user_info = await User.get_by_id(id=user.id)
    return user_info

