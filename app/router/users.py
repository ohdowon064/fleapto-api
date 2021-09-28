from fastapi import APIRouter, Body
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.database.schema import UserSchema
from app.model import UserToken, UserUpdate
from app.repository.User import User

router = APIRouter()

@router.get("/me", response_model=UserSchema)
async def get_me(request: Request):
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


@router.put("/user", response_model=UserToken)
async def update_user(request: Request,
                      update_info: UserUpdate = Body(...)):
    user = request.state.user
    updated_user = await User.update(user.id, update_info)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=updated_user
    )
