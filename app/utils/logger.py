import json
import logging
import traceback
from time import time

from fastapi.logger import logger
from fastapi.requests import Request

from app.utils.date_utils import D

logger.setLevel(logging.INFO)

async def api_logger(request: Request, response=None, error=None):
    t = time() - request.state.start
    status_code = error.status_code if error else response.status_code
    error_detail = None
    user = request.state.user
    # body = await request.json()
    body = None
    if error:
        # print("에러에 대하여")
        # print(error.__traceback__.tb_frame.f_lineno)
        # print("에러로그:::", )

        # if request.state.inspect:
        #     frame = request.state.inspect
        #     error_file = frame.f_code.co_filename
        #     error_func = frame.f_code.co_name
        #     error_line = frame.f_lineno
        # else:
        #     error_func = error_file = error_line = "UNKNOWN"
        #
        # error_log = dict(
        #     errorFunc=error_func,
        #     location=f"{str(error_line)} line in {error_file}",
        #     raised=str(error.__class__.__name__),
        #     msg=str(error.ex)
        # )

        error_detail = traceback.format_exc()

    user_log = dict(
        client=request.state.ip,
        name=user.name if user and user.name else None,
        email=user.email if user and user.email else None,
        address=user.address if user and user.address else None
    )

    log_dict = dict(
        url=request.url.hostname + request.url.path,
        method=str(request.method),
        statusCode=status_code,
        errorDetail=error_detail,
        client=user_log,
        processedTime=str(round(t * 1000, 5)) + "ms",
        datetimeKST=D.timestamp(),
    )


    if body:
        log_dict["body"] = body

    if error:
        logger.error(json.dumps(log_dict))
        # print(log_dict)
    else:
        logger.info(json.dumps(log_dict))