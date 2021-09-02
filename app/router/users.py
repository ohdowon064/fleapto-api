from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

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
    if (user_info := await User.get_by_id(id=user.id)) is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "msg" : "존재하지 않는 사용자 토큰으로 인증을 시도했습니다.",
                "user" : user
            }
        )
    return user_info

