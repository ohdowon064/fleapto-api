import json
import logging
from time import time

from fastapi.logger import logger
from fastapi.requests import Request

from app.utils.date_utils import D

logger.setLevel(logging.INFO)

async def api_logger(request: Request, response=None, error=None):
    t = time() - request.state.start
    status_code = error.status_code if error else response.status_code
    error_log = None
    user = request.state.user
    body = await request.body()
    if error:
        if request.state.inspect:
            frame = request.state.inspect
            error_file = frame.f_code.co_filename
            error_func = frame.f_code.co_name
            error_line = frame.f_lineno
        else:
            error_func = error_file = error_line = "UNKNOWN"

        error_log = dict(
            errorFunc=error_func,
            location=f"{str(error_line)} line in {error_file}",
            raised=str(error.__class__.__name__),
            msg=str(error.ex)
        )

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
        errorDetail=error_log,
        client=user_log,
        processedTime=str(round(t * 1000, 5)) + "ms",
        datetimeKST=D.timestamp(),
    )

    if body:
        log_dict["body"] = body
    if error and error.status_code >= 500:
        logger.error(json.dumps(log_dict))
    else:
        logger.info(json.dumps(log_dict))