import re
import time
from os import environ

import jwt
from jwt import ExpiredSignatureError, DecodeError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.consts import EXCEPT_PATH_REGEX, EXCEPT_PATH_LIST, EXCEPT_API
from app.errors import exceptions as ex
from app.errors.exceptions import APIException
from app.model import UserToken

from app.utils.date_utils import D
from decouple import config

from app.utils.logger import api_logger


async def access_control(request: Request, call_next):
    request.state.req_time = D.kstnow()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None
    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip
    headers = request.headers
    cookies = request.cookies
    root_path = request.scope.get("root_path")
    url = request.url.path.replace(root_path, "")
    request_target = (url, request.method)

    if await url_pattern_check(url, EXCEPT_PATH_REGEX) or url in EXCEPT_PATH_LIST or EXCEPT_API.get(request_target, False):
        response = await call_next(request)
        if url != "/":
            await api_logger(request=request, response=response)
        return response

    try:
        if url.startswith("/api"):
            # api인 경우 헤더로 토큰 검사
            if "authorization" in headers.keys():
                token_info = await token_decode(access_token=headers.get("Authorization"))
                token_info["_id"] = token_info["id"]
                request.state.user = UserToken(**token_info)

            # 토큰 없음
            else:
                if "Authorization" not in headers.keys():
                    raise ex.NotAuthorized()

        else:
            # 템플릿 렌더링인 경우 쿠키에서 토큰 검사
            cookies["Authorization"] = "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjYxMmY0YjkzMmYxMjM2ZWZmNWQ1YzIzYSIsImVtYWlsIjoicm9vdEBleGFtcGxlLmNvbSIsIm5hbWUiOiJyb290Iiwibmlja25hbWUiOiJyb290IiwiYWRkcmVzcyI6InJvb3QifQ.92wubFWw8djzIVID_wbutAaOmVVYWtGjbDjHAMwY4ws"

            if "Authorization" not in cookies.keys():
                raise ex.NotAuthorized()

            token_info = await token_decode(access_token=cookies.get("Authorization"))
            request.state.user = UserToken(**token_info)

        response = await call_next(request)
        await api_logger(request=request, response=response)

    except Exception as e:
        error = await exception_handler(e)
        error_dict = dict(
            status=error.status_code,
            msg=error.msg,
            detail=error.detail,
            code=error.code
        )
        response = JSONResponse(status_code=error.status_code, content=error_dict)
        await api_logger(request=request, error=error)

    return response



async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False

async def token_decode(access_token):
    """
    :param access_token:
    :return:
    """
    try:
        access_token = access_token.replace("JWT ", "")
        payload = jwt.decode(access_token, key=config("JWT_SECRET"), algorithms=[config("JWT_ALGORITHM")])
    except ExpiredSignatureError:
        raise ex.TokenExpiredEx()
    except DecodeError:
        raise ex.TokenDecodeEx()
    return payload

async def exception_handler(error: Exception):
    if not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))
    return error